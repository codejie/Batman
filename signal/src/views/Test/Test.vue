<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { ContentWrap } from '@/components/ContentWrap'
import { DataParam, KLinePanel4, ShowParam } from '@/components/KLine'
import { ElButton } from 'element-plus'


// function getDateString(date: string, days: number): string {
//   if (days == 0)
//     return date
//   const tmp = new Date(Date.parse(date))
//   tmp.setDate(tmp.getDate() + days)
//   return tmp.toISOString().slice(0, 10)
// }

const chartData = ref<DataParam>()
const showParam = ref<ShowParam>({
  maLines: [5, 10, 12],
  markLines: true,
  hideKLine: false,
  hideVolume: false
})

function updateChartParam() {
  const start = '2023-06-01'
  const end = '2023-10-01'

  chartData.value = {
    code: '002236',
    start: start,
    end: end
  }
}

onMounted(() => {
  updateChartParam()
})

function onTestClick() {
  console.log('click')
  // showParam.value.hideVolume = true
  // showParam.value.hideKLine = true
  showParam.value = {
    maLines: [5, 10, 12],
    markLines: true,
    hideKLine: !showParam.value.hideKLine,
    hideVolume: !showParam.value.hideVolume
  }
}

</script>
<template>
  <ContentWrap title="Test">
    <div><ElButton @click="onTestClick">Test</ElButton></div>
    <KLinePanel4 :code="'002236'" />
  </ContentWrap>
</template>