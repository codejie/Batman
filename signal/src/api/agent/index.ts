/**
 * Agent API Endpoints
 */
import request from '@/axios'
import * as Types from './types'
import { PATH_URL } from '@/axios/service'
import { useUserStoreWithOut } from '@/store/modules/user'

export * from './types'

/**
 * Submit a chat message to the agent.
 * @param data Chat request with message and thinking preference
 * @returns Promise with chat response (result code)
 */
export const apiAgentChat = (
    data: Types.ChatRequest
): Promise<IResponse<Types.ChatResponse>> => {
    return request.post({ url: '/agent/chat', data })
}

/**
 * Connects to the SSE endpoint for agent chat responses and handles incoming messages.
 * @param onMessage A callback function to execute when a message is received
 * @param onError A callback function to execute when an error occurs
 * @returns The EventSource instance, allowing you to close the connection manually
 *
 * @example
 * const eventSource = apiConnectToAgent(
 *   (data) => {
 *     if (data.type === 'thinking') {
 *       console.log('Thinking:', data.content)
 *     } else if (data.type === 'content') {
 *       console.log('Response:', data.content)
 *     } else if (data.type === 'finish') {
 *       console.log('Done!')
 *     }
 *   },
 *   (error) => console.error('SSE Error:', error)
 * )
 */
export const apiConnectToAgent = (
    onMessage: (data: Types.AgentSSEPayload) => void,
    onError?: (error: Event) => void
): EventSource => {
    const token = useUserStoreWithOut().getTokenKey
    if (!token) {
        console.error('No token found, cannot connect to SSE.')
    }

    const url = `${PATH_URL}/sse/agent?token=${token}`
    const eventSource = new EventSource(url, { withCredentials: false })

    // Handle default message events (data: {...})
    eventSource.onmessage = (event) => {
        try {
            const parsedData: Types.AgentSSEPayload = JSON.parse(event.data)
            onMessage(parsedData)
        } catch (e) {
            console.error('Failed to parse SSE data:', e)
        }
    }

    // Handle custom events (event: action, data: {...})
    eventSource.addEventListener('action', (event) => {
        try {
            const parsedData: Types.SSEEventData = JSON.parse(event.data)
            onMessage(parsedData)
        } catch (e) {
            console.error('Failed to parse SSE action event:', e)
        }
    })

    eventSource.onerror = (error) => {
        console.error('EventSource failed:', error)
        if (onError) {
            onError(error)
        }
        eventSource.close()
    }

    return eventSource
}

/**
 * Disconnect from the agent SSE endpoint.
 * @param eventSource The EventSource instance to close
 *
 * @example
 * apiDisconnectFromAgent(eventSource)
 */
export const apiDisconnectFromAgent = (eventSource: EventSource | null) => {
    if (eventSource) {
        eventSource.close()
    }
}
