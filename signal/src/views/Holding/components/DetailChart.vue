<script setup lang="ts">
import { HistoryData } from '@/api/data';
import { ProfitTraceItem } from '@/calc/holding';
import KLineChart4 from '@/components/KLine/src/KLineChart4.vue';
import { onMounted, ref, watch } from 'vue';

const props = defineProps({
  profitData: {
    type: Array as () => ProfitTraceItem[],
    required: true
  },
  historyData: {
    type: Array as () => HistoryData[],
    required: true
  },
  width: {
    type: [String, Number],
    default: '100%'
  },
  height: {
    type: [String, Number],
    default: '500px'
  }
})

let xData: string[] = []
let klineData: any[] = []
let volumeData: any[] = []

const kline = ref<InstanceType<typeof KLineChart4>>()

function calcKLineData(data: HistoryData[]) {
  xData = data.map(item => item.日期)
  klineData = data.map(item => [item.开盘, item.收盘, item.最低, item.最高])
  volumeData = data.map(item => [item.日期, item.成交量])

  console.log('xData', xData)
  console.log('klineData', klineData) 
  console.log('volumeData', volumeData)
}

// function updateKLineOptions() {
//   kline.value?.reset()
//   kline.value?.addGrid(0, '4%', '4%', '4%', '40%')
//   kline.value?.addGrid(1, '4%', '70%', '4%', '6%')

//   kline.value?.addAxis(0, xData, true)
//   kline.value?.addAxis(1, xData, false)
//   kline.value?.addAxisPointer([0, 1])

//   kline.value?.addKLine(0, 'KLine', klineData, true, true)

//   kline.value?.addBar(1, 'Volume', volumeData, true)
// }

function resetKLine() {
  kline.value?.reset()
  kline.value?.addGrid(0, '0%', '0%', '0%', '40%')
  kline.value?.addGrid(1, '0%', '70%', '0%', '0%')
}

function setKLineData(data: HistoryData[]) {
  calcKLineData(data)

  kline.value?.addAxis(0, xData, true)
  kline.value?.addAxis(1, xData, false)
  kline.value?.addAxisPointer([0, 1])

  kline.value?.addKLine(0, 'KLine', klineData, true, true)

  kline.value?.addBar(1, 'Volume', volumeData, true)
}

onMounted(() => {
  // calcKLineData(props.historyData)
  // updateKLineOptions()
  resetKLine()
})

watch(
  () => props.historyData,
  (value) => {
    setKLineData(value)
})

</script>
<template>
  <KLineChart4 ref="kline" height="100%" />
</template>