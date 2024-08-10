<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { ContentWrap } from '@/components/ContentWrap'
import { ReqParam, KLineChart3, ShowParam } from '@/components/KLine'
import { ElButton } from 'element-plus'
import { apiHistory } from '@/api/data/stock';
import { HistoryDataModel } from '@/api/data/stock/types';
import { apiMACD } from '@/api/libs/talib';

const klc3 = ref(null)

let historyData: HistoryDataModel[]
let xData
let klineData
let volumeData

let history2: HistoryDataModel[]
let xData2
let klineData2
let volumeData2

onMounted(async () => {
  const ret = await apiHistory({
    code: '002236',
    start: '2024-01-01'
  })
  historyData = ret.result

  const ret2 = await apiHistory({
    code: '002025',
    start: '2024-01-01'    
  })
  history2 = ret2.result
  updateData(historyData, history2)
})

function updateData(data: HistoryDataModel[], data2: HistoryDataModel[]) {
  xData = data.map(item => item.date)
  klineData = data.map(({open, close, low, high}) => ([open, close, low, high]))
  volumeData = data.map(item => [item.date, item.volume, item.open > item.close ? 1 : -1])

  xData2 = data2.map(item => item.date)
  klineData2 = data2.map(({open, close, low, high}) => ([open, close, low, high]))
  volumeData2 = data2.map(item => [item.date, item.volume, item.open > item.close ? 1 : -1])
}

function calcMAData(ma: number, data: number[]) {
  var result: any[] = [];
  for (var i = 0, len = data.length; i < len; i++) {
    if (i < ma) {
      result.push(Number.NaN)
      continue;
    }
    var sum = 0;
    for (var j = 0; j < ma; j++) {
      sum += +data[i - j]
    }
    result.push(sum / ma)
  }
  return result
}

async function fetchMACDData(data: number[]) {
  const ret = await apiMACD({
    value: data    
  })
  console.log(ret.result)
  const arrayData = ret.result.data
  const macd = arrayData.map(item => item[0])
  const signal = arrayData.map(item => item[1])
  const history = arrayData.map(item => item[2])
  // console.log(macd)
  klc3.value?.addLine('DIF', macd)
  klc3.value?.addLine('DEA', signal)
  klc3.value?.addBar('MACD', history)
}

async function fetchMACDData2(data: number[]) {
  const ret = await apiMACD({
    value: data,
    fast: 12,
    slow: 26,
    period: 7
  })
  console.log(ret.result)
  const arrayData = ret.result.data
  const macd = arrayData.map(item => item[0])
  const signal = arrayData.map(item => item[1])
  const history = arrayData.map(item => item[2])
  // console.log(macd)
  klc3.value?.addLine('DIF2', macd)
  klc3.value?.addLine('DEA2', signal)
  klc3.value?.addBar('MACD2', history)
}



function onTestClick() {
  console.log('click')

  klc3.value?.setDate(xData)
  // klc3.value.setKLine(klineData, true, true)
}

function onTest1Click() {
  const closeData = klineData.map(item => item[1])
  // const data = calcMAData(5, closeData)
  // klc3.value?.addLine('ma5', data, true)
  const data9 = calcMAData(9, closeData)
  klc3.value?.addLine('ma9', data9, true)
}

function onTest2Click() {
  // klc3.value?.removeLine('ma5')
  const closeData2 = klineData2.map(item => item[1])
  const data92 = calcMAData(9, closeData2)
  klc3.value?.addLine('ma9', data92, true)
}

function onTest3Click() {
  const closeData = klineData.map(item => item[1])
  console.log(closeData)
  fetchMACDData(closeData)
}

function onTest4Click() {
  const closeData = klineData.map(item => item[1])
  console.log(closeData)
  fetchMACDData2(closeData)
}

</script>
<template>
  <ContentWrap title="Test">
    <div>
      <ElButton @click="onTestClick">Test</ElButton>
      <ElButton @click="onTest1Click">Test1</ElButton>
      <ElButton @click="onTest2Click">Test2</ElButton>
      <ElButton @click="onTest3Click">Test3</ElButton>
      <ElButton @click="onTest4Click">Test4</ElButton>
    </div>
    <!-- <KLinePanel :param="param" :show-table="true" /> -->
    <KLineChart3 ref="klc3" />
  </ContentWrap>
</template>