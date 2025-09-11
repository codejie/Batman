<script setup lang="ts">
import { computed, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import { ElButton } from 'element-plus'
import { useTrendStore } from '@/store/modules/calcReport'
import { useTagsView } from '@/hooks/web/useTagsView'
import { useTagsViewStore } from '@/store/modules/tagsView'

const router = useRouter()
const route = useRoute()
const trendStore = useTrendStore()
const { closeCurrent } = useTagsView()
const tagsViewStore = useTagsViewStore()

const chartId = route.params.id as string

const data = computed(() => trendStore.getReportData(chartId))

// watch(
//   data,
//   (newData) => {
//     if (newData) {
//       console.log('Data from router:', JSON.parse(JSON.stringify(newData)))
//     }
//   },
//   { immediate: true, deep: true }
// )

const title = computed(() => {
  if (!data.value) return '聚合图表'
  return `${data.value.stock.name} (${data.value.stock.code}) - 聚合图表`
})

const goBack = () => {
  router.back()
}

const handleClose = () => {
  closeCurrent()
  const visitedViews = tagsViewStore.getVisitedViews
  const latestView = visitedViews.slice(-1)[0]
  if (latestView) {
    router.push(latestView.fullPath)
  } else {
    router.push('/')
  }
}


</script>

<template>
  <ContentDetailWrap :title="title">
    <template #header>
      <div>
        <ElButton type="primary" @click="goBack">返回</ElButton>
        <ElButton type="danger" @click="handleClose">关闭</ElButton>
      </div>
    </template>
    <div v-if="data" class="p-4">
      <p class="mb-4">Data received. Check the browser console for details.</p>
      <pre>{{ JSON.stringify(data, null, 2) }}</pre>
    </div>
    <div v-else class="p-4 text-center text-gray-500">
      <p>No data available. Please go back and select a report.</p>
    </div>
  </ContentDetailWrap>
</template>