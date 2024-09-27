<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { ContentWrap } from '@/components/ContentWrap'
import { ReqParam, KLineChart4, ShowParam, KLinePanel2 } from '@/components/KLine'
import { ElButton } from 'element-plus'
import { apiHistory } from '@/api/data/stock';
import { HistoryDataModel } from '@/api/data/stock/types';
import { apiMACD } from '@/api/libs/talib';
import { Echart, EChartsOption } from '@/components/Echart'

// const klc3 = ref(null)

// let historyData: HistoryDataModel[]
// let xData
// let klineData
// let volumeData

// let history2: HistoryDataModel[]
// let xData2
// let klineData2
// let volumeData2

// onMounted(async () => {
//   const ret = await apiHistory({
//     code: '002236',
//     start: '2024-01-01'
//   })
//   historyData = ret.result

//   const ret2 = await apiHistory({
//     code: '002025',
//     start: '2024-01-01'    
//   })
//   history2 = ret2.result
//   updateData(historyData, history2)
// })

// function updateData(data: HistoryDataModel[], data2: HistoryDataModel[]) {
//   xData = data.map(item => item.date)
//   klineData = data.map(({open, close, low, high}) => ([open, close, low, high]))
//   volumeData = data.map(item => [item.date, item.volume, item.open < item.close ? 1 : -1])

//   xData2 = data2.map(item => item.date)
//   klineData2 = data2.map(({open, close, low, high}) => ([open, close, low, high]))
//   volumeData2 = data2.map(item => [item.date, item.volume, item.open < item.close ? 1 : -1])
// }

// function calcMAData(ma: number, data: number[]) {
//   var result: any[] = [];
//   for (var i = 0, len = data.length; i < len; i++) {
//     if (i < ma) {
//       result.push(Number.NaN)
//       continue;
//     }
//     var sum = 0;
//     for (var j = 0; j < ma; j++) {
//       sum += +data[i - j]
//     }
//     result.push(sum / ma)
//   }
//   return result
// }

// async function fetchMACDData(data: number[]) {
//   const ret = await apiMACD({
//     value: data    
//   })
//   // console.log(ret.result)
//   const arrayData = ret.result.data
//   const macd = arrayData.map(item => item[0])
//   const signal = arrayData.map(item => item[1])
//   const history = arrayData.map(item => item[2])
//   // console.log(macd)
//   klc3.value?.addLine('DIF', macd)
//   klc3.value?.addLine('DEA', signal)
//   klc3.value?.addBar('MACD', history)
// }

// async function fetchMACDData2(data: number[]) {
//   const ret = await apiMACD({
//     value: data,
//     fast: 12,
//     slow: 26,
//     period: 7
//   })
//   // console.log(ret.result)
//   const arrayData = ret.result.data
//   const macd = arrayData.map(item => item[0])
//   const signal = arrayData.map(item => item[1])
//   const history = arrayData.map(item => item[2])
//   // console.log(macd)
//   klc3.value?.addLine('DIF2', macd)
//   klc3.value?.addLine('DEA2', signal)
//   klc3.value?.addBar('MACD2', history)
// }


// function onTestClick() {
//   console.log('click')

//   // klc3.value?.setDate(xData)
//   // klc3.value.setKLine(klineData, true, true)
//   // klc3.value?.addGrid(0, '2%', '2%', '2%', '50%')
//   // klc3.value?.addGrid(1, '2%', '60%', '2%', '8%')
//   // klc3.value?.addAxis(0, xData, true)
//   // klc3.value?.addKLine(0, 'K', klineData, true, true)
//   // klc3.value?.addAxis(1, xData, false)

//   klc3.value?.addAxisPointer([0, 1])
// }

// function onTest1Click() {
//   const closeData = klineData.map(item => item[1])
//   klc3.value?.addLine(0, 'close', closeData)
//   klc3.value?.addBar(1, 'volumn', volumeData)
//   // const data = calcMAData(5, closeData)
//   // klc3.value?.addLine('ma5', data, true)
//   // const data9 = calcMAData(9, closeData)
//   // klc3.value?.addLine('ma9', data9, true)
//   // klc3.value?.setLayout(3)
// }

// function onTest2Click() {
//   // klc3.value?.removeLine('ma5')
//   // const closeData2 = klineData2.map(item => item[1])
//   // const data92 = calcMAData(9, closeData2)
//   // klc3.value?.addLine('ma9', data92, true)
//   klc3.value?.reset()
// }

// function onTest3Click() {
//   klc3.value?.remove('volumn')
//   // const closeData = klineData.map(item => item[1])
//   // console.log(closeData)
//   // fetchMACDData(closeData)

// }

// function onTest4Click() {
//   // const closeData = klineData.map(item => item[1])
//   // console.log(closeData)
//   // fetchMACDData2(closeData)
//   param.value = {
//     code: '000001'
//   }
// }

// const param = ref<ReqParam>({
//   code: '002236'
// })

const upColor = '#ec0000'
const downColor = '#00da3c'

const options = ref<EChartsOption>({
  title: {
    text: 'Step Line'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Step Start', 'Step Middle', 'Step End']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  toolbox: {
    feature: {
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'Step Start',
      type: 'line',
      step: 'start',
      data: [120, 132, 101, 134, 90, 230, 210]
    },
    {
      name: 'Step Middle',
      type: 'line',
      step: 'middle',
      data: [220, 282, 201, 234, 290, 430, 410]
    },
    {
      name: 'Step End',
      type: 'line',
      step: 'end',
      data: [['Mon', 450], ['Wed', 432], ['Sat', 530], ['Sun', 510]]
    }
  ] 
})

</script>
<template>
  <ContentWrap title="Test">
    <!-- <div>
      <ElButton @click="onTestClick">Test</ElButton>
      <ElButton @click="onTest1Click">Test1</ElButton>
      <ElButton @click="onTest2Click">Test2</ElButton>
      <ElButton @click="onTest3Click">Test3</ElButton>
      <ElButton @click="onTest4Click">Test4</ElButton>
    </div> -->
    <!-- <KLinePanel :param="param" :show-table="true" /> -->
    <!-- <KLineChart4 ref="klc3" /> -->
      <!-- <KLinePanel2 :req-param="param" /> -->
    <Echart :options="options" />
  </ContentWrap>
</template>