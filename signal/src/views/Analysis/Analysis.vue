<script setup lang="ts">
import { ContentWrap } from '@/components/ContentWrap'
import { ElInput, ElButton } from 'element-plus'
import { ref, onUnmounted } from 'vue'
import { useUserStoreWithOut } from '@/store/modules/user';

// refer to https://github.com/DR-lin-eng/stock-scanner

const messages = ref<string[]>([])
const eventSource = ref<EventSource | null>(null)

const connect = () => {
  const token = useUserStoreWithOut().getTokenKey
  if (!token) {
    console.error('No token found, cannot connect to SSE.')
    return
  }

  // Append the token as a query parameter
  const url = `http://localhost:8000/agent/report?token=${token}`
  console.log('Connecting to SSE at:', url)
  eventSource.value = new EventSource(url)

  eventSource.value.onmessage = (event) => {
    messages.value.push(event.data)
  }

  eventSource.value.onerror = (error) => {
    console.error('EventSource failed:', error)
    eventSource.value?.close()
  }
}

onUnmounted(() => {
  if (eventSource.value) {
    eventSource.value.close()
    console.log('EventSource connection closed.')
  }
})
</script>
<template>
  <ContentWrap>
    <ElButton @click="connect">连接</ElButton>
    <ElInput
      :model-value="messages.join('\n')"
      type="textarea"
      :rows="10"
      readonly
      placeholder="等待接收消息…"
    ></ElInput>
  </ContentWrap>
</template>

