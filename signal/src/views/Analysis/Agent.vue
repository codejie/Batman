<script setup lang="ts">
import { ref, onBeforeUnmount, nextTick } from 'vue'
import { ElSelect, ElOption, ElButton, ElMessage, ElIcon, ElSpace, ElInput, ElEmpty } from 'element-plus'
import { ContentWrap } from '@/components/ContentWrap'
import { apiAgentChat, apiConnectToAgent, apiDisconnectFromAgent, SSEMessageTypeLabels } from '@/api/agent'
import type { ChatRequest, SSEMessage } from '@/api/agent'

interface ChatMessage {
  type: 'user' | 'thinking' | 'assistant' | 'error'
  content: string
  timestamp?: string
}

const useThinking = ref(false)
const userMessage = ref('')
const chatMessages = ref<ChatMessage[]>([])
const isLoading = ref(false)
const messagesContainerRef = ref<HTMLDivElement>()
let eventSource: EventSource | null = null

const sendMessage = async () => {
  if (!userMessage.value.trim()) {
    ElMessage.warning('请输入消息')
    return
  }

  // Add user message to chat
  chatMessages.value.push({
    type: 'user',
    content: userMessage.value,
    timestamp: new Date().toLocaleTimeString()
  })

  const message = userMessage.value
  userMessage.value = ''
  isLoading.value = true

  try {
    // Send chat request
    const chatRequest: ChatRequest = {
      message,
      use_thinking: useThinking.value
    }

    const res = await apiAgentChat(chatRequest)
    if (res && res.code === 0) {
      // Connect to SSE for streaming response
      eventSource = apiConnectToAgent(
        (data) => {
          if ('type' in data && data.type) {
            const sseMessage = data as SSEMessage
            
            if (sseMessage.type === 'thinking') {
              const lastMessage = chatMessages.value[chatMessages.value.length - 1]
              if (lastMessage && lastMessage.type === 'thinking') {
                lastMessage.content += sseMessage.content || ''
              } else {
                chatMessages.value.push({
                  type: 'thinking',
                  content: sseMessage.content || '',
                  timestamp: new Date().toLocaleTimeString()
                })
              }
            } else if (sseMessage.type === 'content') {
              // Find the last assistant message or create a new one
              const lastMessage = chatMessages.value[chatMessages.value.length - 1]
              if (lastMessage && lastMessage.type === 'assistant') {
                lastMessage.content += sseMessage.content || ''
              } else {
                chatMessages.value.push({
                  type: 'assistant',
                  content: sseMessage.content || '',
                  timestamp: new Date().toLocaleTimeString()
                })
              }
            } else if (sseMessage.type === 'finish') {
              isLoading.value = false
            } else if (sseMessage.type === 'error') {
              chatMessages.value.push({
                type: 'error',
                content: sseMessage.content || sseMessage.reason || '发生错误',
                timestamp: new Date().toLocaleTimeString()
              })
              isLoading.value = false
            } else if (sseMessage.type === 'chart') {
              // Handle chart message type if needed
              chatMessages.value.push({
                type: 'assistant',
                content: '[图表数据已接收]',
                timestamp: new Date().toLocaleTimeString()
              })
            }
            
            // Scroll to bottom
            nextTick(() => {
              if (messagesContainerRef.value) {
                messagesContainerRef.value.scrollTop = messagesContainerRef.value.scrollHeight
              }
            })
          }
        },
        (error) => {
          console.error('SSE connection error:', error)
          chatMessages.value.push({
            type: 'error',
            content: '连接失败，请重试',
            timestamp: new Date().toLocaleTimeString()
          })
          isLoading.value = false
        }
      )
    } else {
      ElMessage.warning(res?.code === 1 ? '任务已在运行中' : '发送失败')
      isLoading.value = false
    }
  } catch (error) {
    console.error('Error sending message:', error)
    chatMessages.value.push({
      type: 'error',
      content: '发送出错，请重试',
      timestamp: new Date().toLocaleTimeString()
    })
    isLoading.value = false
  }
}

const clearMessages = () => {
  chatMessages.value = []
}

onBeforeUnmount(() => {
  if (eventSource) {
    apiDisconnectFromAgent(eventSource)
  }
})

const getMessageClass = (type: string) => {
  const classMap: Record<string, string> = {
    user: 'message-user',
    assistant: 'message-assistant',
    thinking: 'message-thinking',
    error: 'message-error'
  }
  return classMap[type] || ''
}
</script>

<template>
  <ContentWrap>
    <div class="agent-container">
      <!-- Messages Display -->
      <div class="messages-container" ref="messagesContainerRef">
        <ElEmpty v-if="chatMessages.length === 0" description="暂无消息，开始对话吧" />
        
        <div v-for="(msg, index) in chatMessages" :key="index" :class="`message ${getMessageClass(msg.type)}`">
          <div class="message-header">
            <span class="message-type">{{ SSEMessageTypeLabels[msg.type] || msg.type }}</span>
            <span class="message-time" v-if="msg.timestamp">{{ msg.timestamp }}</span>
          </div>
          <div class="message-content">{{ msg.content }}</div>
        </div>

        <div v-if="isLoading" class="loading-indicator">
          <span>正在处理中...</span>
        </div>
      </div>

      <!-- Input Panel -->
      <div class="input-panel">
        <div class="input-area">
          <ElInput
            v-model="userMessage"
            type="textarea"
            :rows="3"
            placeholder="请输入你的问题或指令..."
            :disabled="isLoading"
            @keyup.ctrl.enter="sendMessage"
          />
        </div>

        <div class="button-area">
          <ElSpace>
            <span class="text-sm">启用思考：</span>
            <ElSelect v-model="useThinking" style="width: 80px" size="small">
              <ElOption :label="'否'" :value="false" />
              <ElOption :label="'是'" :value="true" />
            </ElSelect>
          </ElSpace>
          <ElSpace>
            <ElButton type="primary" :loading="isLoading" @click="sendMessage">
              发送 (Ctrl+Enter)
            </ElButton>
            <ElButton @click="clearMessages" :disabled="isLoading">
              清空消息
            </ElButton>
          </ElSpace>
        </div>
      </div>
    </div>
  </ContentWrap>
</template>

<style scoped lang="less">
.agent-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 200px);
  gap: 16px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  background-color: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  gap: 8px;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: #f1f1f1;
  }

  &::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 3px;

    &:hover {
      background: #999;
    }
  }
}

.message {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  word-break: break-word;

  &.message-user {
    align-self: flex-end;
    max-width: 70%;
    background-color: #e6f7ff;
    border-left: 3px solid #1890ff;
  }

  &.message-assistant {
    align-self: flex-start;
    max-width: 70%;
    background-color: #f6f8fb;
    border-left: 3px solid #409eff;
  }

  &.message-thinking {
    align-self: flex-start;
    max-width: 70%;
    background-color: #fef0f6;
    border-left: 3px solid #f56c6c;
    font-style: italic;
    opacity: 0.8;
  }

  &.message-error {
    align-self: flex-start;
    max-width: 70%;
    background-color: #fef0f0;
    border-left: 3px solid #f56c6c;
    color: #f56c6c;
  }
}

.message-header {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #666;
}

.message-type {
  font-weight: 500;
}

.message-time {
  color: #999;
}

.message-content {
  white-space: pre-wrap;
  line-height: 1.5;
}

.loading-indicator {
  align-self: flex-start;
  padding: 8px 12px;
  color: #666;
  font-style: italic;
}

.input-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.input-area {
  width: 100%;
}

.button-area {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
