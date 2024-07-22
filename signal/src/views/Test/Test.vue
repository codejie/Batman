<script setup lang="ts">
import KLinePanel, { DataParam, ShowParam } from '@/components/KLine/src/KLinePanel.vue';
import { onMounted, ref } from 'vue';
import { ContentWrap } from '@/components/ContentWrap'


function getDateString(date: string, days: number): string {
  if (days == 0)
    return date
  const tmp = new Date(Date.parse(date))
  tmp.setDate(tmp.getDate() + days)
  return tmp.toISOString().slice(0, 10)
}

const chartData = ref<DataParam>()
const showParam = ref<ShowParam>({
  maLines: [5, 10, 12, 24]
})

function updateChartParam() {
  const start = '2023-01-01'
  const end = '2024-01-01'

  chartData.value = {
    code: '002236',
    start: start,
    end: end
  }
}

onMounted(() => {
  updateChartParam()
})

</script>
<template>
  <ContentWrap title="Test">
    <KLinePanel :data="chartData" :show="showParam"/>
  </ContentWrap>
</template>