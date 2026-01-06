/**
 * Agent API Constants and Definitions
 */

// SSE Message type labels
export const SSEMessageTypeLabels = {
    thinking: '🤔 Thinking',
    content: '💬 Response',
    finish: '✓ Finish',
    error: '❌ Error'
}

// Error messages
export const AgentErrorMessages = {
    NO_TOKEN: 'No authentication token found',
    TASK_RUNNING: 'Agent task already running for this user',
    INVALID_MESSAGE: 'Invalid message format',
    SSE_CONNECTION_FAILED: 'Failed to establish SSE connection',
    UNKNOWN_ERROR: 'An unexpected error occurred'
}
