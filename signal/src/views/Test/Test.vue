<script setup lang="ts">
import { historyApi } from '@/api/data/stock';
import { HistoryDataModel } from '@/api/data/stock/types';
import { ContentWrap } from '@/components/ContentWrap'
import { Echart, EChartsOption } from '@/components/Echart'
import { useUserStoreWithOut } from '@/store/modules/user';
import { onMounted, ref, unref } from 'vue';

// const data = ref<HistoryDataModel[]>()
const upColor = '#ec0000';
const downColor = '#00da3c';

// const xData = ref<string[]>([])
const userStore = useUserStoreWithOut()

const barOptions = ref<EChartsOption>({
  title: [],
  grid: [
    {
      left: '10%',
      right: '8%',
      height: '50%',
      top: '5%'
    },
    {
      left: '10%',
      right: '8%',
      top: '60%',
      height: '30%'
    }     
  ],
  xAxis:[
    {
      type: 'category',
      gridIndex: 0,
      // name: 'Date',
      // inverse: true,
      data: []
    },
    {
      type: 'category',
      gridIndex: 1,
      // name: 'Date',
      data: [],
      boundaryGap: false,
      axisLine: { onZero: false },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      // min: 'dataMin',
      // max: 'dataMax'
    }        
  ],
  yAxis: [
    {
      type: 'value',
      name: 'Value',
      nameLocation : 'middle',
      show: true,
      gridIndex: 0,
      position: 'left',
      nameGap: 15,
      // inverse: true
      scale: true
    },
    {
      type: 'value',
      name: 'Volume',
      nameLocation : 'middle',
      show: true,
      gridIndex: 1,
      position: 'left',
      nameGap: 15,
      // inverse: true
      scale: true,
      splitNumber: 1,
      axisLabel: { show: false },
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { show: false }
    }     
  ],
  series: [
    {
      name: 'Stock Data',
      type: 'candlestick',
      itemStyle: {
        color: upColor,
        color0: downColor,
        borderColor: undefined,
        borderColor0: undefined
      },
      xAxisIndex: 0,
      yAxisIndex: 0,
      // data: data.map(({open, close, low, high}) => ([open, close, low, high]))
      data: []
    },
    {
      name: 'Volume',
      type: 'bar',
      xAxisIndex: 1,
      yAxisIndex: 1,
      data: []
    }      
  ],
  visualMap: {
    show: false,
    seriesIndex: 1,
    dimension: 2,
    pieces: [
      {
        value: 1,
        color: downColor
      },
      {
        value: -1,
        color: upColor
      }
    ]
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    },
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    textStyle: {
      color: '#000'
    },
    position: function (pos, params, el, elRect, size) {
      const obj = {
        top: 10
      };
      obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
      return obj;
    }
  },  
  axisPointer: {
    link: [
      {
        xAxisIndex: [0, 1]
      }
    ],
    label: {
      backgroundColor: '#777'
    }
  },    
})

function updateOpt(data: HistoryDataModel[]) {
  const xData = data.map(item => item.date)
  barOptions.value.xAxis![0].data = xData
  barOptions.value.xAxis![1].data = xData
  barOptions.value.series![0].data = data.map(({open, close, low, high}) => ([open, close, low, high]))
  barOptions.value.series![1].data = data.map(item => [item.date, item.volume, item.open < item.close ? 1 : -1])
}

onMounted(async () => {
  const ret = await historyApi({
    code: '002236',
    start: '2023-10-01',
    end: '2024-01-01'
  })
  // data.value = ret.result
  // const x =  ret.result.map(item => [item.volume, -1])
  // console.log(x)
  updateOpt(ret.result)
  // xa.value = unref(data)?.map(item => item.date)
  // y.value = unref(data)?.map(({open, close, low, high}) => ([open, close, low, high]))
})
</script>
<template>
  <ContentWrap title="Test">
    <!-- {{  userStore.getUserInfo?.uid }} -->
    <div>
      <Echart :options="barOptions" />
    </div>
  </ContentWrap>
</template>