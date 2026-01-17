<script setup lang="ts">
import { ref, nextTick, reactive } from 'vue'
import {
  ElSelect,
  ElOption,
  ElButton,
  ElMessage,
  ElSpace,
  ElInput,
  ElEmpty,
  ElDrawer,
  ElForm,
  ElFormItem,
  ElSwitch,
  ElInputNumber,
  ElCollapse,
  ElCollapseItem
} from 'element-plus'
import { Setting } from '@element-plus/icons-vue'
import { ContentWrap } from '@/components/ContentWrap'
import { DeepSeekAgent, type AgentConfig } from '@/utils/agentHelper'
import { KLineDialog, type ReqParam } from '@/components/KLine'

interface ChatMessage {
  type: 'user' | 'thinking' | 'assistant' | 'error'
  content: string
  timestamp?: string
  throttledContent?: string
}

const SSEMessageTypeLabels: Record<string, string> = {
  user: '用户',
  assistant: 'AI助手',
  thinking: '思考中',
  error: '错误'
}

// Agent Configuration
const config = reactive<AgentConfig>({
  name: 'DeepSeek Assistant',
  system_prompt: `- 你是一个专业的股票市场和量化分析师，根据请求提供概要的或详细的股票和市场趋势分析。
  - 你能够通过提供的工具/tools接口来获取股票和市场数据，以提供更准确的分析，和完善的内容，按需要调用，不要重复调用，不用每次都调用。
  - 处理请求前，你需要正确判断请求中的各种日期内容，如‘今天’在日期/date上是今天的‘YYYY-MM-DD’，‘三个月’是指‘最近的三个月’等，以保证数据准确性。
  - 请求中要求图表输出或应答中含有图标输出时，以JSON格式返回图表数据所需的参数信息，不需要返回具体图表的数据，内容参考如下，并在输出前添加”\n@@START@@"，在输出后添加"\n@@END@@"，用于前端获取图表配置后进行渲染。
    { 
      "info": {
        "type": 2, 
        "name": "中国平安",
        "code": "0000001",
        "start": "2020-01-01",
        "end": "2020-05-01",
        "period": "daily"
      },
      "chart": {
        "type": "kline", // kline/line/bar/candlestick/mixed
        "xAxis": ["日期"],
        "yAxis": ["K线数据"] //Y轴数据指示，可以是多个，如["K线数据","成交量"]
      }
    }
  `,
  //'You are a helpful assistant with access to tools.',
  apiKey: localStorage.getItem('deepseek_api_key') || '',
  model: 'deepseek-chat',
  temperature: 0.7,
  max_tokens: 2000,
  top_p: 1.0,
  memory: {
    enabled: true,
    max_history: 20
  },
  tools: [] // Will be populated from agent
})

const isConfigVisible = ref(false)
const showSettings = () => {
  isConfigVisible.value = true
}

const saveConfig = () => {
  localStorage.setItem('deepseek_api_key', config.apiKey)
  // Update agent with current UI tool status
  if (config.tools) {
    config.tools.forEach(t => {
      agent.setToolEnabled(t.name, !!t.enabled)
    })
  }
  isConfigVisible.value = false
  ElMessage.success('配置已保存')
}

// Agent Instance
const agent = new DeepSeekAgent(config)

// Initialize tools from agent's internal scanning
config.tools = agent.getAvailableTools()

const isLoading = ref(false)
const useThinking = ref(false)
const showThinking = ref(true)
const autoShowChart = ref(true)
const userMessage = ref('')
const chatMessages = ref<ChatMessage[]>([])
const activeNames = ref([])
const messagesContainerRef = ref<HTMLDivElement>()

// KLine Dialog State
const klineDialogVisible = ref(false)
const klineReqParam = ref<ReqParam | undefined>(undefined)

const triggerKLine = (jsonStr: string) => {
  if (!jsonStr) return
  try {
    console.log('KLine trigger from text:', jsonStr)
    const data = JSON.parse(jsonStr)
    const info = data.info || data
    if (info && info.code && info.type !== undefined) {
      klineReqParam.value = {
        type: Number(info.type),
        name: info.name,
        code: String(info.code),
        start: info.start,
        end: info.end,
        period: info.period,
        // adjust: info.adjust
      }
      console.log('KLine param set:', klineReqParam.value)
      klineDialogVisible.value = true
    }
  } catch (e) {
    console.warn('Failed to parse throttled content as JSON for KLine trigger:', e)
  }
}

// Content Filtering Logic
class ContentFilter {
  public isFiltering = false
  public filteredContentTotal = ''
  private startDelimiter = '@@START@@'
  private endDelimiter = '@@END@@'
  private buffer = ''

  public process(chunk: string): string {
    this.buffer += chunk
    let visibleResult = ''

    while (this.buffer.length > 0) {
      if (!this.isFiltering) {
        const startIndex = this.buffer.indexOf(this.startDelimiter)
        if (startIndex === -1) {
          const safeLength = Math.max(0, this.buffer.length - this.startDelimiter.length + 1)
          visibleResult += this.buffer.substring(0, safeLength)
          this.buffer = this.buffer.substring(safeLength)
          break
        } else {
          visibleResult += this.buffer.substring(0, startIndex)
          this.isFiltering = true
          this.buffer = this.buffer.substring(startIndex + this.startDelimiter.length)
        }
      } else {
        const endIndex = this.buffer.indexOf(this.endDelimiter)
        if (endIndex === -1) {
          const safeLength = Math.max(0, this.buffer.length - this.endDelimiter.length + 1)
          this.filteredContentTotal += this.buffer.substring(0, safeLength)
          this.buffer = this.buffer.substring(safeLength)
          break
        } else {
          this.filteredContentTotal += this.buffer.substring(0, endIndex)
          this.isFiltering = false
          this.buffer = this.buffer.substring(endIndex + this.endDelimiter.length)
        }
      }
    }
    return visibleResult
  }

  public reset() {
    this.isFiltering = false
    this.filteredContentTotal = ''
    this.buffer = ''
  }
}

const contentFilter = new ContentFilter()

const sendMessage = async () => {
  if (!config.apiKey) {
    ElMessage.warning('请先在配置中设置 API Key')
    showSettings()
    return
  }

  if (!userMessage.value.trim()) {
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

  // Update agent config before sending
  agent.updateConfig({
    ...config,
    model: useThinking.value ? 'deepseek-reasoner' : 'deepseek-chat'
  })

  // Reset filter state
  contentFilter.reset()

  try {
    await agent.chat(
      message,
      (sseMessage) => {
        if (sseMessage.type === 'thinking') {
          if (showThinking.value) {
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
          }
        } else if (sseMessage.type === 'content') {
          const visibleContent = contentFilter.process(sseMessage.content || '')
          
          const lastMessage = chatMessages.value[chatMessages.value.length - 1]
          if (lastMessage && lastMessage.type === 'assistant') {
            lastMessage.content += visibleContent
            // Always update throttledContent if something was captured
            if (contentFilter.filteredContentTotal) {
              lastMessage.throttledContent = contentFilter.filteredContentTotal
            }
          } else {
            chatMessages.value.push({
              type: 'assistant',
              content: visibleContent,
              throttledContent: contentFilter.filteredContentTotal || undefined,
              timestamp: new Date().toLocaleTimeString()
            })
          }
        } else if (sseMessage.type === 'finish') {
          isLoading.value = false
          
          // Automatic KLine Trigger
          if (contentFilter.filteredContentTotal && autoShowChart.value) {
            triggerKLine(contentFilter.filteredContentTotal)
          }
        } else if (sseMessage.type === 'error') {
          chatMessages.value.push({
            type: 'error',
            content: sseMessage.content || '发生错误',
            timestamp: new Date().toLocaleTimeString()
          })
          isLoading.value = false
        }

        // Scroll to bottom
        nextTick(() => {
          if (messagesContainerRef.value) {
            messagesContainerRef.value.scrollTop = messagesContainerRef.value.scrollHeight
          }
        })
      },
      (error) => {
        console.error('Chat error:', error)
        chatMessages.value.push({
          type: 'error',
          content: typeof error === 'string' ? error : error.message || '连接失败，请检查 API Key 或网络',
          timestamp: new Date().toLocaleTimeString()
        })
        isLoading.value = false
      }
    )
  } catch (error: any) {
    console.error('Error sending message:', error)
    chatMessages.value.push({
      type: 'error',
      content: error.message || '发送出错，请重试',
      timestamp: new Date().toLocaleTimeString()
    })
    isLoading.value = false
  }
}

const clearMessages = () => {
  chatMessages.value = []
  agent.clearHistory()
}

const getMessageClass = (type: string) => {
  const classMap: Record<string, string> = {
    user: 'message-user',
    assistant: 'message-assistant',
    thinking: 'message-thinking',
    error: 'message-error'
  }
  return classMap[type] || ''
}

const copyToClipboard = (text: string) => {
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制节流内容到剪贴板')
    // Debug: Also try to trigger KLine if it's valid JSON
    triggerKLine(text)
  }).catch(() => {
    ElMessage.error('复制失败')
  })
}
</script>

<template>
  <ContentWrap>
    <div class="agent-container">
      <!-- Header with Settings -->
      <div class="agent-header">
        <span class="title">DeepSeek AI 助手</span>
        <ElButton :icon="Setting" circle @click="showSettings" />
      </div>

      <!-- Messages Display -->
      <div class="messages-container" ref="messagesContainerRef">
        <ElEmpty v-if="chatMessages.length === 0" description="暂无消息，开始对话吧" />
        
        <div v-for="(msg, index) in chatMessages" :key="index" :class="`message ${getMessageClass(msg.type)}`">
          <div class="message-header">
            <span class="message-type">{{ SSEMessageTypeLabels[msg.type] || msg.type }}</span>
            <span class="message-time" v-if="msg.timestamp">{{ msg.timestamp }}</span>
          </div>
          <div class="message-content">{{ msg.content }}</div>
          <div v-if="msg.throttledContent" class="throttled-action">
            <ElButton size="small" type="info" link @click="copyToClipboard(msg.throttledContent)">
              图表数据 ({{ msg.throttledContent.length }})
            </ElButton>
          </div>
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
            @keyup.enter.native="sendMessage"
          />
        </div>

        <div class="button-area">
          <ElSpace>
            <span class="text-xs">启用深度思考：</span>
            <ElSwitch v-model="useThinking" size="small" />
            <span class="text-xs">显示思考内容：</span>
            <ElSwitch v-model="showThinking" size="small" />
            <span class="text-xs">自动显示图表：</span>
            <ElSwitch v-model="autoShowChart" size="small" />
          </ElSpace>
          <ElSpace>
            <ElButton type="primary" :loading="isLoading" @click="sendMessage">
              发送 (Enter)
            </ElButton>
            <ElButton @click="clearMessages" :disabled="isLoading">
              清空消息
            </ElButton>
          </ElSpace>
        </div>
      </div>
    </div>

    <!-- Configuration Drawer -->
    <ElDrawer
      v-model="isConfigVisible"
      title="Agent 配置"
      direction="rtl"
      size="450px"
    >
      <ElForm :model="config" label-width="100px">
        <ElFormItem label="API Key">
          <ElInput v-model="config.apiKey" type="password" show-password placeholder="DeepSeek API Key" />
        </ElFormItem>
        <ElFormItem label="模型">
          <ElSelect v-model="config.model" style="width: 100%">
            <ElOption label="deepseek-chat" value="deepseek-chat" />
            <ElOption label="deepseek-reasoner" value="deepseek-reasoner" />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="系统提示词">
          <ElInput v-model="config.system_prompt" type="textarea" :rows="4" />
        </ElFormItem>
        <ElFormItem label="温度 (Temp)">
          <ElInputNumber v-model="config.temperature" :step="0.1" :min="0" :max="2" />
        </ElFormItem>
        <ElFormItem label="最大 Token">
          <ElInputNumber v-model="config.max_tokens" :step="500" :min="100" :max="8000" />
        </ElFormItem>
        <ElFormItem label="历史记忆数">
          <ElInputNumber v-if="config.memory" v-model="config.memory.max_history" :min="1" :max="100" />
        </ElFormItem>

        <!-- Tools Collapse at the bottom -->
        <div style="margin-top: 20px">
          <ElCollapse v-model="activeNames">
            <ElCollapseItem title="扩展工具管理" name="1">
              <div class="tools-list">
                <div v-for="tool in config.tools" :key="tool.name" class="tool-item">
                  <div class="tool-info">
                    <span class="tool-name">{{ tool.name }}</span>
                    <span class="tool-desc">{{ tool.description }}</span>
                  </div>
                  <ElSwitch v-model="tool.enabled" />
                </div>
              </div>
            </ElCollapseItem>
          </ElCollapse>
        </div>

        <div style="margin-top: 20px; text-align: right">
          <ElButton @click="isConfigVisible = false">取消</ElButton>
          <ElButton type="primary" @click="saveConfig">保存</ElButton>
        </div>
      </ElForm>
    </ElDrawer>

    <!-- KLine Dialog -->
    <KLineDialog
      v-if="klineReqParam"
      v-model:visible="klineDialogVisible"
      :req-param="klineReqParam"
      @update:onClose="klineDialogVisible = false"
    />
  </ContentWrap>
</template>

<style scoped lang="less">
.tools-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
}

.tool-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 4px;

  .tool-info {
    display: flex;
    flex-direction: column;
    
    .tool-name {
      font-size: 13px;
      font-weight: bold;
      color: #409eff;
    }
    
    .tool-desc {
      font-size: 11px;
      color: #909399;
    }
  }
}
.agent-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 200px);
  gap: 16px;
}

.agent-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 4px;
  
  .title {
    font-size: 18px;
    font-weight: bold;
    color: #303133;
  }
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
  background-color: #f9f9f9;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 12px;

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
  gap: 6px;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
  max-width: 85%;
  word-break: break-word;

  &.message-user {
    align-self: flex-end;
    background-color: #e6f7ff;
    border: 1px solid #91d5ff;
    color: #000;
  }

  &.message-assistant {
    align-self: flex-start;
    background-color: #fff;
    border: 1px solid #dcdfe6;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }

  &.message-thinking {
    align-self: flex-start;
    background-color: #fffaf0;
    border: 1px dashed #e6a23c;
    color: #e6a23c;
    font-style: italic;
  }

  &.message-error {
    align-self: flex-start;
    background-color: #fef0f0;
    border: 1px solid #fbc4c4;
    color: #f56c6c;
  }
}

.message-header {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: #909399;
  margin-bottom: 2px;
}

.message-type {
  font-weight: bold;
}

.message-time {
  opacity: 0.8;
}

.message-content {
  white-space: pre-wrap;
}

.throttled-action {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed #ebeef5;
  text-align: right;
}

.loading-indicator {
  align-self: flex-start;
  padding: 8px 12px;
  color: #909399;
  font-size: 13px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

.input-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background-color: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.02);
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
