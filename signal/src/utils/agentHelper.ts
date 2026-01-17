/**
 * DeepSeek Agent implementation in frontend.
 * Provides capabilities to interact with DeepSeek API directly.
 */

export interface ToolConfig {
  name: string
  description: string
  parameters?: Record<string, any>
  enabled?: boolean
}

export interface MemoryConfig {
  max_history?: number
  enabled?: boolean
}

export interface AgentConfig {
  name: string
  system_prompt: string
  apiKey: string
  model?: string
  temperature?: number
  max_tokens?: number
  top_p?: number
  memory?: MemoryConfig
  tools?: ToolConfig[]
}

export interface Message {
  role: 'user' | 'assistant' | 'system' | 'tool'
  content: string
  reasoning_content?: string
  tool_calls?: any[]
  tool_call_id?: string
  name?: string
}

export type SSEMessageType = 'thinking' | 'content' | 'finish' | 'error'

export interface SSEMessage {
  type: SSEMessageType
  content?: string
  reason?: string
}

export type ToolHandler = (args: any) => Promise<any> | any

export interface ToolDefinitionWithHandler extends ToolConfig {
  handler: ToolHandler
}

export class DeepSeekAgent {
  private config: AgentConfig
  private conversationHistory: Message[] = []
  private baseUrl = 'https://api.deepseek.com'
  private availableTools: ToolDefinitionWithHandler[] = []

  constructor(config: AgentConfig) {
    this.config = {
      model: 'deepseek-chat',
      temperature: 0.7,
      top_p: 1.0,
      memory: { enabled: true, max_history: 10 },
      ...config
    }
    this.loadLocalTools()
  }

  /**
   * Scans AgentTools directory for tool definitions.
   * Uses Vite's import.meta.glob for eager loading.
   */
  private loadLocalTools() {
    try {
      // @ts-ignore
      const modules = import.meta.glob('./AgentTools/*.ts', { eager: true })
      const allTools: ToolDefinitionWithHandler[] = []

      for (const path in modules) {
        // Skip files that contain 'skip' in their name
        if (path.toLowerCase().includes('skip')) {
          continue
        }

        const module = modules[path] as any
        if (module.tools && Array.isArray(module.tools)) {
          allTools.push(...module.tools)
        }
      }
      this.availableTools = allTools

      // Sync enabled status from config if provided
      if (this.config.tools) {
        this.config.tools.forEach(configTool => {
          const tool = this.availableTools.find(t => t.name === configTool.name)
          if (tool) {
            tool.enabled = configTool.enabled
          }
        })
      }
    } catch (e) {
      console.error('Failed to load local tools:', e)
    }
  }

  public getAvailableTools(): ToolConfig[] {
    return this.availableTools.map(({ handler, ...rest }) => rest)
  }

  public setToolEnabled(name: string, enabled: boolean) {
    const tool = this.availableTools.find(t => t.name === name)
    if (tool) {
      tool.enabled = enabled
    }
  }

  public updateConfig(newConfig: Partial<AgentConfig>) {
    this.config = { ...this.config, ...newConfig }
    // Update local tools enabled status if config tools are updated
    if (newConfig.tools) {
      newConfig.tools.forEach(configTool => {
        const tool = this.availableTools.find(t => t.name === configTool.name)
        if (tool) {
          tool.enabled = configTool.enabled
        }
      })
    }
  }

  public getConfig(): AgentConfig {
    // Return config with updated tool statuses
    return {
      ...this.config,
      tools: this.getAvailableTools()
    }
  }

  public clearHistory() {
    this.conversationHistory = []
  }

  private addMessage(message: Message) {
    this.conversationHistory.push(message)
    if (this.config.memory?.enabled) {
      const maxHistory = this.config.memory.max_history || 10
      if (this.conversationHistory.length > maxHistory) {
        this.conversationHistory = this.conversationHistory.slice(-maxHistory)
      }
    }
  }

  private getMessagesForApi() {
    const messages: any[] = [
      { role: 'system', content: this.config.system_prompt }
    ]

    this.conversationHistory.forEach(msg => {
      const apiMsg: any = {
        role: msg.role,
        content: msg.content
      }
      if (msg.reasoning_content) {
        apiMsg.reasoning_content = msg.reasoning_content
      }
      if (msg.tool_calls) {
        apiMsg.tool_calls = msg.tool_calls
      }
      if (msg.tool_call_id) {
        apiMsg.tool_call_id = msg.tool_call_id
      }
      if (msg.name) {
        apiMsg.name = msg.name
      }
      messages.push(apiMsg)
    })

    return messages
  }

  private getToolSchemas() {
    return this.availableTools
      .filter((t) => t.enabled !== false)
      .map((t) => ({
        type: 'function',
        function: {
          name: t.name,
          description: t.description,
          parameters: t.parameters
        }
      }))
  }

  /**
   * Chat with the agent and stream the response.
   */
  public async chat(
    userMessage: string | null,
    onMessage: (data: SSEMessage) => void,
    onError?: (error: any) => void
  ) {
    try {
      if (userMessage) {
        this.addMessage({ role: 'user', content: userMessage })
      }

      let shouldContinue = true
      while (shouldContinue) {
        const messages = this.getMessagesForApi()
        const toolSchemas = this.getToolSchemas()

        const response = await fetch(`${this.baseUrl}/chat/completions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${this.config.apiKey}`
          },
          body: JSON.stringify({
            model: this.config.model,
            messages: messages,
            temperature: this.config.temperature,
            top_p: this.config.top_p,
            max_tokens: this.config.max_tokens,
            tools: toolSchemas && toolSchemas.length > 0 ? toolSchemas : undefined,
            stream: true
          })
        })

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(errorData.error?.message || `HTTP error! status: ${response.status}`)
        }

        const reader = response.body!.getReader()
        const decoder = new TextDecoder()
        let fullContent = ''
        let fullReasoning = ''
        let isThinking = false
        let buffer = ''
        let currentToolCalls: any[] = []
        let finishReason = ''

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop() || ''

          for (const line of lines) {
            const trimmedLine = line.trim()
            if (!trimmedLine || !trimmedLine.startsWith('data: ')) continue

            const dataStr = trimmedLine.slice(6)
            if (dataStr === '[DONE]') continue

            try {
              const data = JSON.parse(dataStr)
              const delta = data.choices[0].delta
              finishReason = data.choices[0].finish_reason

              if (delta.reasoning_content) {
                isThinking = true
                fullReasoning += delta.reasoning_content
                onMessage({ type: 'thinking', content: delta.reasoning_content })
              }

              if (delta.content) {
                if (isThinking) isThinking = false
                fullContent += delta.content
                onMessage({ type: 'content', content: delta.content })
              }

              if (delta.tool_calls) {
                for (const tc of delta.tool_calls) {
                  if (!currentToolCalls[tc.index]) {
                    currentToolCalls[tc.index] = { id: '', type: 'function', function: { name: '', arguments: '' } }
                  }
                  if (tc.id) currentToolCalls[tc.index].id += tc.id
                  if (tc.function?.name) currentToolCalls[tc.index].function.name += tc.function.name
                  if (tc.function?.arguments) currentToolCalls[tc.index].function.arguments += tc.function.arguments
                }
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e)
            }
          }
        }

        if (finishReason === 'tool_calls' || currentToolCalls.length > 0) {
          // Add assistant message with tool calls
          this.addMessage({
            role: 'assistant',
            content: fullContent,
            reasoning_content: fullReasoning,
            tool_calls: currentToolCalls
          })

          for (const toolCall of currentToolCalls) {
            const name = toolCall.function.name
            const argsJSON = toolCall.function.arguments
            let args = {}
            try {
              args = JSON.parse(argsJSON)
            } catch (e) {
              console.error('Failed to parse tool arguments:', argsJSON)
            }

            onMessage({ type: 'thinking', content: `> 调用工具: ${name}(${JSON.stringify(args)})\n` })

            const tool = this.availableTools.find(t => t.name === name)
            let result
            if (tool && tool.handler) {
              try {
                result = await tool.handler(args)
              } catch (e: any) {
                result = `错误: ${e.message}`
              }
            } else {
              result = `错误: 工具 ${name} 未找到或处理器丢失`
            }

            this.addMessage({
              role: 'tool',
              tool_call_id: toolCall.id,
              name: name,
              content: typeof result === 'string' ? result : JSON.stringify(result)
            })

            onMessage({ type: 'thinking', content: `> 工具返回: ${JSON.stringify(result)}\n` })
          }
          // Continue loop to send tool results back to LLM
        } else {
          if (fullContent || fullReasoning) {
            this.addMessage({
              role: 'assistant',
              content: fullContent,
              reasoning_content: fullReasoning
            })
          }
          onMessage({ type: 'finish', reason: finishReason })
          shouldContinue = false
        }
      }
    } catch (error: any) {
      console.error('Agent chat error:', error)
      if (onError) onError(error)
      else onMessage({ type: 'error', content: error.message || 'Unknown error' })
    }
  }
}
