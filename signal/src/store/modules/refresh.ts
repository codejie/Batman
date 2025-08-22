import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useRefreshStore = defineStore('refresh', () => {
  const needsRefresh = ref(false)

  const setNeedsRefresh = (status: boolean) => {
    needsRefresh.value = status
  }

  return {
    needsRefresh,
    setNeedsRefresh
  }
})