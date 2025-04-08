<script setup lang="ts">
import { HistoryData } from '@/api/data';
import { ProfitTraceItem } from '@/calc/holding';
import { KLineChart5 } from '@/components/KLine';
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
let quantityData: any[] = []

const kline = ref<InstanceType<typeof KLineChart5>>()

function calcKLineData(data: HistoryData[]) {
  xData = data.map(item => item.日期)
  klineData = data.map(item => [item.开盘, item.收盘, item.最低, item.最高])
  volumeData = data.map(item => [item.日期, item.成交量])

  // console.log('xData', xData)
  // console.log('klineData', klineData) 
  // console.log('volumeData', volumeData)
}

function calcProfitData(data: ProfitTraceItem[]) {
  quantityData = data.map(item => [item.date, item.quantity])
}

function resetKLine() {
  kline.value?.reset()
  kline.value?.addGrid(0, '2%', '0%', '2%', '35%')
  kline.value?.addGrid(1, '%', '75%', '2%', '10%')
}

function setKLineData() {
  kline.value?.addAxis(0, xData, 'left', true)
  // kline.value?.addAxis(0, xData, 'right', true)
  // kline.value?.addAxis(1, xData, false)
  // kline.value?.addAxisPointer([0, 1])

  // kline
  kline.value?.addKLine(0, 0, 'KLine', klineData, true, true)
  // profit
  // kline.value?.addBar(0, 'Quantity', quantityData, true)
  // volume
  // kline.value?.addBar(1, 2, 'Volume', volumeData, true)
}

onMounted(() => {
  resetKLine()
})

watch(
  () => props.historyData,
  (value) => {
    calcKLineData(value)
    setKLineData()
})

// watch(
//   () => props.profitData,
//   (value) => {
//     calcProfitData(value)
//     setKLineData()
// })

</script>
<template>
  <KLineChart5 class="my-4" ref="kline" :height="height" />
</template>