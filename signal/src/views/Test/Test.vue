<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { ContentWrap } from '@/components/ContentWrap'
import { ReqParam, KLineChart3, ShowParam } from '@/components/KLine'
import { ElButton } from 'element-plus'


// function getDateString(date: string, days: number): string {
//   if (days == 0)
//     return date
//   const tmp = new Date(Date.parse(date))
//   tmp.setDate(tmp.getDate() + days)
//   return tmp.toISOString().slice(0, 10)
// }

const chartData = ref<ReqParam>()
const showParam = ref<ShowParam>({
  maLines: [],
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

const param = ref<any>({
  code: '002236',
  name: '一二三四'
})

function onTestClick() {
  console.log('click')
  // showParam.value.hideVolume = true
  // showParam.value.hideKLine = true
  // showParam.value = {
  //   maLines: [5, 10, 12],
  //   markLines: true,
  //   hideKLine: !showParam.value.hideKLine,
  //   hideVolume: !showParam.value.hideVolume
  // }
  klc3.value?.setDateData(['2023-01-01', '2023-01-02'])
}

const klc3 = ref(null)

</script>
<template>
  <ContentWrap title="Test">
    <div><ElButton @click="onTestClick">Test</ElButton></div>
    <!-- <KLinePanel :param="param" :show-table="true" /> -->
     <KLineChart3 ref="klc3"/>
  </ContentWrap>
</template>