<script setup lang="ts">
import { ref, onUnmounted, computed, defineProps, watch } from 'vue'
import { ElButton } from 'element-plus'
import ArgumentDisplay from './ArgumentDisplay.vue'
import {
  apiConnectToCalcReport,
  apiDisconnectFromCalcReport,
  apiListArguments
} from '@/api/calc'
import type { ArgumentItem, CalcReportSseData, SsePayload } from '@/api/calc'

const props = defineProps<{itemId: number}>()

interface ActionPayload {
  action: 'start' | 'log' | 'finish'
  message?: string
}

interface CategoryGroup {
  category: number
  types: number[]
}

const eventSource = ref<EventSource | null>(null)
const messages = ref<string[]>([])
const isSseConnected = ref(false)
const logMessage = ref<string>('Waiting for calculation to start...')
const argumentList = ref<ArgumentItem[]>([])
const categoryGroups = ref<CategoryGroup[]>([])

const messagesText = computed(() => messages.value.join('\n'))

const fetchArguments = async (id: number) => {
  if (!id) return
  try {
    const res = await apiListArguments({ cid: id })
    if (res) {
      argumentList.value = res.result
      console.log('Fetched arguments:', argumentList.value)

      // Group arguments by category
      const groups: { [key: number]: number[] } = {}
      for (const item of argumentList.value) {
        if (!groups[item.category]) {
          groups[item.category] = []
        }
        groups[item.category].push(item.type)
      }

      categoryGroups.value = Object.entries(groups).map(([category, types]) => ({
        category: Number(category),
        types: types
      }))
      console.log('Processed category groups:', categoryGroups.value)
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
  logMessage.value = 'Connecting...'
  isSseConnected.value = true
  eventSource.value = apiConnectToCalcReport(
    (data: SsePayload<CalcReportSseData>) => {
      messages.value.push(JSON.stringify(data, null, 2))
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
            console.log('SSE action: start')
            logMessage.value = 'Calculation started...'
            break
          case 'log':
            if (payload.message) {
              logMessage.value = payload.message
            }
            break
          case 'finish':
            console.log('SSE action: finish')
            logMessage.value = 'Calculation finished.'
            break
        }
      } catch (error) {
        console.error('Error parsing SSE action event data:', error)
        // Also push raw data for debugging
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
    <div class="text-component">
      <p>{{ logMessage }}</p>
    </div>
    <ArgumentDisplay :argument-list="argumentList" />
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
