<script setup lang="ts">
import { ref, onUnmounted, computed, defineProps, watch } from 'vue'
import { ElButton } from 'element-plus'
import CalcReportItem from './CalcReportItem.vue'
import { apiConnectToCalcReport, apiDisconnectFromCalcReport, apiListArguments } from '@/api/calc'
import type { ArgumentItem, CalcReportSseData } from '@/api/calc'

const props = defineProps<{itemId: number}>()

// SSE action payload
interface ActionPayload {
  action: 'start' | 'log' | 'finish'
  message?: string
}

// Aggregated structure for reports per stock
export interface AggregatedReport {
  stock: {
    type: number
    code: string
    name: string
  }
  reports: {
    category: number
    type: number
    report: any
  }[]
}

const eventSource = ref<EventSource | null>(null)
const messages = ref<string[]>([])
// Use an array for reportItems
const reportItems = ref<AggregatedReport[]>([])
const isSseConnected = ref(false)
const logMessage = ref<string>('Waiting for calculation to start...')
const argumentList = ref<ArgumentItem[]>([])

const messagesText = computed(() => messages.value.join('\n'))

const fetchArguments = async (id: number) => {
  if (!id) return
  try {
    const res = await apiListArguments({ cid: id })
    if (res) {
      argumentList.value = res.result
    }
  } catch (error) {
    console.error('Error fetching arguments:', error)
  }
}

watch(
  () => props.itemId,
  (newId) => {
    if (newId) {
      fetchArguments(newId)
    }
  },
  { immediate: true }
)

const connect = () => {
  if (eventSource.value) {
    return // Already connected
  }

  messages.value = ['Connecting to SSE...']
  reportItems.value = [] // Reset data on new connection
  logMessage.value = 'Connecting...'
  isSseConnected.value = true

  eventSource.value = apiConnectToCalcReport(
    (data: CalcReportSseData) => {
      messages.value.push(JSON.stringify(data, null, 2))

      const stockCode = data.stock.code
      const stockType = data.stock.type
      const stockEntry = reportItems.value.find(
        (item) => item.stock.code === stockCode && item.stock.type === stockType
      )

      if (stockEntry) {
        // If found, push the new report
        stockEntry.reports.push({
          category: data.category,
          type: data.type,
          report: data.report
        })
      } else {
        // If not found, create a new entry and push it to the array
        const newEntry: AggregatedReport = {
          stock: data.stock,
          reports: [
            {
              category: data.category,
              type: data.type,
              report: data.report
            }
          ]
        }
        reportItems.value.push(newEntry)
      }
    },
    (error) => {
      console.error('SSE connection error:', error)
      messages.value.push('SSE connection error.')
      logMessage.value = 'SSE connection error.'
      disconnect()
    }
  )

  if (eventSource.value) {
    eventSource.value.addEventListener('action', (event: Event) => {
      const messageEvent = event as MessageEvent<string>
      try {
        const payload: ActionPayload = JSON.parse(messageEvent.data)
        switch (payload.action) {
          case 'start':
            logMessage.value = 'Calculation started...'
            break
          case 'log':
            if (payload.message) {
              logMessage.value = payload.message
            }
            break
          case 'finish':
            logMessage.value = 'Calculation finished.'
            disconnect()
            break
        }
      } catch (error) {
        console.error('Error parsing SSE action event data:', error)
        messages.value.push(messageEvent.data)
      }
    })
  }
}

const disconnect = () => {
  if (eventSource.value) {
    apiDisconnectFromCalcReport(eventSource.value)
    eventSource.value = null
    messages.value.push('SSE connection closed.')
    logMessage.value = 'Disconnected.'
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
    <div class="text-component" v-if="isSseConnected">
      <p><small>{{ logMessage }}</small></p>
    </div>

    <div class="report-items-container" v-if="reportItems.length > 0">
      <CalcReportItem
        v-for="item in reportItems"
        :key="item.stock.code"
        :data="item"
      />
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
.text-component {
  margin-bottom: 1rem;
}
.report-items-container {
  margin-bottom: 1rem;
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
