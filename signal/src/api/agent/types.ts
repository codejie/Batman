/**
 * Agent API Types
 */

// Chat request/response types
export interface ChatRequest {
    message: string
    use_thinking?: boolean
}

export interface ChatResponse {
    result: number // 0 for success, 1 if task already running
}

// SSE Message types
export type SSEMessageType = 'thinking' | 'content' | 'finish' | 'error'

export interface SSEMessage {
    type: SSEMessageType
    content?: string
    reason?: string
}

export interface SSEEventData {
    action: string
    message?: string
}

// Combined SSE payload types
export type AgentSSEPayload = SSEMessage | SSEEventData

export const SSEMessageTypeLabels: Record<string, string> = {
    user: '用户',
    assistant: 'AI助手',
    thinking: '思考中',
    error: '错误'
}
