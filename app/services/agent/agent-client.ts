/**
 * DeepSeek Agent API Client
 * 用于与 Batman 后端的 Agent API 交互
 */

export interface ToolConfig {
    name: string;
    description: string;
    parameters?: Record<string, any>;
    enabled?: boolean;
}

export interface MemoryConfig {
    max_history?: number;
    memory_type?: "message_window" | "summary";
    enabled?: boolean;
}

export interface AgentConfig {
    name: string;
    system_prompt: string;
    tools?: ToolConfig[];
    memory?: MemoryConfig;
    model?: string;
    temperature?: number;
    max_tokens?: number;
    top_p?: number;
    top_k?: number;
}

export interface ChatRequest {
    config: AgentConfig;
    message: string;
    use_thinking?: boolean;
}

export interface ChatResponse {
    code: number;
    message: string;
    result: number; // 0 = success, 1 = task already running
}

export type SSEMessageType = "thinking" | "content" | "finish" | "error";

export interface SSEMessage {
    type: SSEMessageType;
    content?: string;
    reason?: string;
}

export interface SSEEvent {
    action: string;
    message?: string;
}

/**
 * DeepSeek Agent 客户端
 */
export class AgentClient {
    private baseURL: string;
    private token: string;
    private uid: number;

    constructor(baseURL: string = "http://localhost:8000", token?: string, uid?: number) {
        this.baseURL = baseURL;
        this.token = token || "";
        this.uid = uid || 0;
    }

    /**
     * 设置认证令牌
     */
    setToken(token: string): void {
        this.token = token;
    }

    /**
     * 设置用户 ID
     */
    setUID(uid: number): void {
        this.uid = uid;
    }

    /**
     * 获取请求头
     */
    private getHeaders(): Record<string, string> {
        return {
            "Content-Type": "application/json",
            ...(this.token ? { Authorization: `Bearer ${this.token}` } : {}),
        };
    }

    /**
     * 提交聊天请求
     */
    async submitChat(request: ChatRequest): Promise<ChatResponse> {
        const response = await fetch(`${this.baseURL}/agent/chat`, {
            method: "POST",
            headers: this.getHeaders(),
            body: JSON.stringify(request),
        });

        if (!response.ok) {
            throw new Error(`Chat request failed: ${response.statusText}`);
        }

        return response.json();
    }

    /**
     * 监听 SSE 响应
     * @param onMessage 收到消息时的回调
     * @param onEvent 收到事件时的回调
     * @param onError 错误时的回调
     * @param onComplete 完成时的回调
     */
    listenToSSE(
        onMessage?: (msg: SSEMessage) => void,
        onEvent?: (event: SSEEvent) => void,
        onError?: (error: Error) => void,
        onComplete?: () => void
    ): EventSource {
        const url = new URL(`${this.baseURL}/sse/agent`);
        if (this.uid) {
            url.searchParams.set("uid", this.uid.toString());
        }

        const eventSource = new EventSource(url.toString());

        // 处理 action 事件
        eventSource.addEventListener("action", (event) => {
            try {
                const data = JSON.parse(event.data);
                onEvent?.(data);

                if (data.action === "finish") {
                    onComplete?.();
                    eventSource.close();
                } else if (data.action === "error") {
                    onError?.(new Error(data.message || "Unknown error"));
                }
            } catch (e) {
                onError?.(e as Error);
            }
        });

        // 处理 data 事件（默认）
        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data) as SSEMessage;
                onMessage?.(data);
            } catch (e) {
                onError?.(e as Error);
            }
        };

        // 处理错误
        eventSource.onerror = () => {
            const error = new Error("SSE connection error");
            onError?.(error);
            eventSource.close();
        };

        return eventSource;
    }

    /**
     * 保存配置到文件
     */
    async saveConfig(config: AgentConfig, configPath: string): Promise<{ result: number }> {
        const response = await fetch(`${this.baseURL}/agent/save_config`, {
            method: "POST",
            headers: this.getHeaders(),
            body: JSON.stringify({ config, config_path: configPath }),
        });

        if (!response.ok) {
            throw new Error(`Save config failed: ${response.statusText}`);
        }

        return response.json();
    }

    /**
     * 从文件加载配置
     */
    async loadConfig(configPath: string): Promise<{ result: number; config?: AgentConfig }> {
        const response = await fetch(`${this.baseURL}/agent/load_config`, {
            method: "POST",
            headers: this.getHeaders(),
            body: JSON.stringify({ config_path: configPath }),
        });

        if (!response.ok) {
            throw new Error(`Load config failed: ${response.statusText}`);
        }

        return response.json();
    }
}

/**
 * 高级客户端：自动处理 SSE 连接和消息流
 */
export class AgentChatSession {
    private client: AgentClient;
    private eventSource: EventSource | null = null;
    private messages: { type: string; content: string }[] = [];

    constructor(client: AgentClient) {
        this.client = client;
    }

    /**
     * 开始聊天会话
     */
    async chat(
        request: ChatRequest,
        onChunk?: (chunk: string) => void,
        onThinking?: (thinking: string) => void,
        onComplete?: () => void,
        onError?: (error: Error) => void
    ): Promise<void> {
        // 提交聊天请求
        const response = await this.client.submitChat(request);

        if (response.result !== 0) {
            onError?.(new Error("Task already running or failed to start"));
            return;
        }

        // 监听 SSE 响应
        return new Promise((resolve) => {
            this.eventSource = this.client.listenToSSE(
                (msg) => {
                    if (msg.type === "thinking") {
                        onThinking?.(msg.content || "");
                        this.messages.push({ type: "thinking", content: msg.content || "" });
                    } else if (msg.type === "content") {
                        onChunk?.(msg.content || "");
                        this.messages.push({ type: "content", content: msg.content || "" });
                    }
                },
                (event) => {
                    if (event.action === "finish") {
                        onComplete?.();
                    } else if (event.action === "error") {
                        onError?.(new Error(event.message || "Unknown error"));
                    }
                },
                onError,
                () => {
                    resolve();
                }
            );
        });
    }

    /**
     * 获取收集的消息
     */
    getMessages(): { type: string; content: string }[] {
        return this.messages;
    }

    /**
     * 清除消息
     */
    clearMessages(): void {
        this.messages = [];
    }

    /**
     * 关闭连接
     */
    close(): void {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
        }
    }
}

/**
 * 使用示例：
 *
 * const client = new AgentClient("http://localhost:8000", "your-token", 123);
 *
 * const config: AgentConfig = {
 *   name: "Assistant",
 *   system_prompt: "You are a helpful assistant",
 *   model: "deepseek-chat",
 *   temperature: 0.7,
 * };
 *
 * const session = new AgentChatSession(client);
 *
 * try {
 *   await session.chat(
 *     { config, message: "Hello!", use_thinking: true },
 *     (chunk) => console.log("Content:", chunk),
 *     (thinking) => console.log("Thinking:", thinking),
 *     () => console.log("Complete!"),
 *     (error) => console.error("Error:", error)
 *   );
 * } catch (error) {
 *   console.error("Chat failed:", error);
 * }
 */
