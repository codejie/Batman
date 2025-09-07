<script setup lang="ts">
import { ref, onUnmounted, defineProps, watch, computed } from 'vue'
import { ElButton, ElTabs, ElTabPane } from 'element-plus'
import CalcReportItem from './CalcReportItem.vue'
import { apiConnectToCalcReport, apiDisconnectFromCalcReport, apiListArguments } from '@/api/calc'
import type { ArgumentItem, CalcReportData } from '@/api/calc'

const props = defineProps<{itemId: number, dataPeriod: number}>()

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
    category: string
    type: string
    calc: any
    report: any[]
    arguments: any
  }[]
}

const eventSource = ref<EventSource | null>(null)
// Use an array for reportItems
const reportItems = ref<AggregatedReport[]>([])
const isSseConnected = ref(false)
const logMessage = ref<string>('Waiting for calculation to start...')
const argumentList = ref<ArgumentItem[]>([])

const displayMode = ref<'tile' | 'tab'>('tab')

const toggleDisplayMode = () => {
  displayMode.value = displayMode.value === 'tab' ? 'tile' : 'tab'
}

const displayModeText = computed(() => {
  return displayMode.value === 'tab' ? '平铺展示' : '标签展示'
})

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

  reportItems.value = [] // Reset data on new connection
  logMessage.value = 'Connecting...'
  isSseConnected.value = true

  eventSource.value = apiConnectToCalcReport(
    (data: CalcReportData) => {
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
          calc: data.result.calc,
          report: data.result.report,
          arguments: data.arguments
        })
      } else {
        // If not found, create a new entry and push it to the array
        const newEntry: AggregatedReport = {
          stock: data.stock,
          reports: [
            {
              category: data.category,
              type: data.type,
              calc: data.result.calc,
              report: data.result.report,
              arguments: data.arguments
            }
          ]
        }
        reportItems.value.push(newEntry)
      }
    },
    (error) => {
      console.error('SSE connection error:', error)
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
      }
    })
  }
}

const disconnect = () => {
  if (eventSource.value) {
    apiDisconnectFromCalcReport(eventSource.value)
    eventSource.value = null
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
      <div>
        <span class="section-title">计算结果</span>
        <el-button v-if="reportItems.length > 0" type="primary" size="small" @click="toggleDisplayMode" style="margin-left: 12px;">{{ displayModeText }}</el-button>
      </div>
      <el-button v-if="isSseConnected" type="danger" size="small" @click="disconnect">停止</el-button>
    </div>
    <div class="text-component" v-if="isSseConnected">
      <p><small>{{ logMessage }}</small></p>
    </div>

    <div class="report-items-container" v-if="reportItems.length > 0">
      <div v-if="displayMode === 'tile'">
        <CalcReportItem
          v-for="item in reportItems"
          :key="item.stock.code"
          :data="item"
          :data-period="props.dataPeriod"
        />
      </div>
      <el-tabs v-else>
        <el-tab-pane v-for="item in reportItems" :key="item.stock.code" :label="item.stock.name">
          <CalcReportItem :data="item" :data-period="props.dataPeriod" />
        </el-tab-pane>
      </el-tabs>
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
</style>