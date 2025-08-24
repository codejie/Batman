<script setup lang="ts">
import { ref, onUnmounted, computed } from 'vue'
import { ElButton } from 'element-plus'
import { apiConnectToCalcReport, apiDisconnectFromCalcReport } from '@/api/calc'
import type { CalcReportSseData, SsePayload } from '@/api/calc'

const eventSource = ref<EventSource | null>(null)
const messages = ref<string[]>([])
const isSseConnected = ref(false)

const messagesText = computed(() => messages.value.join('\n'))

const connect = () => {
  if (eventSource.value) {
    return // Already connected
  }

  messages.value = ['Connecting to SSE...']
  isSseConnected.value = true
  eventSource.value = apiConnectToCalcReport(
    (data: SsePayload<CalcReportSseData>) => {
      messages.value.push(JSON.stringify(data, null, 2))
    },
    (error) => {
      console.error('SSE connection error:', error)
      messages.value.push('SSE connection error.')
      disconnect()
    }
  )

  if (eventSource.value) {
    eventSource.value.addEventListener('action', (event: Event) => {
      const messageEvent = event as MessageEvent<string>
      messages.value.push(messageEvent.data)
    })
  }
}

const disconnect = () => {
  if (eventSource.value) {
    apiDisconnectFromCalcReport(eventSource.value)
    eventSource.value = null
    messages.value.push('SSE connection closed.')
    isSseConnected.value = false
  }
}

onUnmounted(() => {
  disconnect()
})

defineExpose({
  connect,
  disconnect
})
</script>

<template>
  <div class="calc-report-view">
    <div class="section-header">
      <div class="section-title">计算结果</div>
      <el-button v-if="isSseConnected" type="danger" size="small" @click="disconnect">停止</el-button>
    </div>
    <div class="sse-display">
      <textarea :value="messagesText" readonly rows="10" style="width: 100%; white-space: pre-wrap;"></textarea>
    </div>
  </div>
</template>

<style scoped>
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.section-title {
  font-size: 16px;
  font-weight: 700;
}
.sse-display {
  margin-top: 1rem;
}
textarea {
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px;
  font-family: monospace;
}
</style>