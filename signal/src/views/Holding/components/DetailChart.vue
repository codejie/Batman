<script setup lang="ts">
import { HistoryData } from '@/api/data';
import { ProfitTraceItem } from '@/calc/holding';
import { Echart } from '@/components/Echart';
import { EChartsOption } from 'echarts';
import { ref, watch } from 'vue';
import * as Calc from '@/calc/data';

const props = defineProps({
  profitData: {
    type: Array as () => ProfitTraceItem[],
    required: true
  },
  historyData: {
    type: Array as () => HistoryData[],
    required: true
  },
  // operationData: {
  //   type: Array as () => OperationItem[],
  //   required: true
  // },
  width: {
    type: [String, Number],
    default: '100%'
  },
  height: {
    type: [String, Number],
    default: '500px'
  }
})

const upColor = '#ec0000'
const downColor = '#00da3c'
const quantityColor = '#aaaaff'
const maItems: number[] = [5, 10, 30, 60]

const xData = ref<string[] | number[]>()
const klineData = ref<any[]>()
const volumeData = ref<any[]>()
const maData = ref<string[][]>([]) // 5, 10, 30, 60

const priceAvgData = ref<string[]>()
const revenueData = ref<number[] | string[]>()
const profitData = ref<number[] | string[]>()
const quantityData = ref<number[]>()

const chartOption = ref<EChartsOption>({
  grid: [
      {
        id: 0,
        left: '4%',
        top: '4%',
        right: '4%',
        bottom: '60%'
      },
      {
        id: 1,
        left: '4%',
        top: '45%',
        right: '4%',
        bottom: '20%'
      },
      {
        id: 2,
        left: '4%',
        top: '85%',
        right: '4%',
        bottom: '2%'
      }
    ],
    xAxis: [
      {
        type: 'category',
        gridIndex: 1,
        // data: xData.value,
        boundaryGap: false,
        axisLine: { onZero: true },
        axisTick: { show: true },
        splitLine: { show: false },
        axisLabel: { show: true }
      },
      {
        type: 'category',
        gridIndex: 2,
        // data: xData.value,
        boundaryGap: false,
        axisLine: { onZero: true },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false }
      },
      {
        type: 'category',
        gridIndex: 0,
        // data: xData.value,
        boundaryGap: false,
        axisLine: { onZero: true },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false }
      }    
    ],
    yAxis: [
      {
        type: 'value', // kline
        // nameLocation : 'middle',
        show: true,
        gridIndex: 1,
        position: 'left',
        nameGap: 30,
        scale: true,
        splitArea: {
          show: true
        },
        splitNumber: 8,
        axisLabel: { show: true },
        axisLine: { show: true },
        axisTick: { show: true },
        splitLine: { show: false }
      },
      {
        type: 'value',
        // nameLocation : 'middle',
        show: true,
        gridIndex: 2,
        position: 'left',
        nameGap: 30,
        scale: true,
        splitArea: {
          show: true
        },
        splitNumber: 8,
        axisLabel: { show: false },
        axisLine: { show: true },
        axisTick: { show: false },
        splitLine: { show: false }
      },
      { // price avg
        type: 'value',
        show: true,
        gridIndex: 0,
        position: 'left',
        alignTicks: true,
        // nameGap: 30,
        scale: true,
        offset: -120,
        // splitArea: {
        //   show: true
        // },
        axisLabel: { show: true },
        axisLine: { show: true },
        axisTick: { show: true },
        splitLine: { show: true }
      },
      { // profit
        type: 'value',
        show: true,
        gridIndex: 0,
        position: 'left',
        alignTicks: true,
        // nameGap: 30,
        offset: -60,
        scale: true,
        // splitArea: {
        //   show: true
        // },
        axisLabel: { show: true },
        axisLine: { show: true },
        axisTick: { show: true },
        splitLine: { show: true }
      },
      { // revenue
        type: 'value',
        show: true,
        gridIndex: 0,
        position: 'left',
        alignTicks: true,
        // nameGap: 30,
        scale: true,
        // splitArea: {
        //   show: true
        // },
        axisLabel: { show: true },
        axisLine: { show: true },
        axisTick: { show: true },
        splitLine: { show: true }
      },      
      { // quantity
        type: 'value',
        show: true,
        gridIndex: 0,
        position: 'right',
        alignTicks: true,
        // nameGap: 30,
        scale: true,
        // splitArea: {
        //   show: true
        // },
        axisLabel: { show: true },
        axisLine: { show: true },
        axisTick: { show: true },
        splitLine: { show: true }
      }
    ],
    axisPointer: {
      link: [
        {
          xAxisIndex: 'all'
        }
      ],
      label: {
        backgroundColor: '#777'
      }
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
      // position: function (pos, params, el, elRect, size) {
      //   const obj = {
      //     top: 10
      //   };
      //   obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
      //   return obj;
      // }    
    },        
    series: [
      {
        type: 'candlestick',
        name: 'Kline',
        itemStyle: {
          color: upColor,
          color0: downColor
        },
        xAxisIndex: 0,
        yAxisIndex: 0,
        markLine: {
          symbol: ['none', 'none'],
          data: []
        },
        // data: klineData.value
      },
      {
        type: 'bar',
        name: 'Volume',
        xAxisIndex: 1,
        yAxisIndex: 1,
        showSymbol: false,
        itemStyle: {
          color: (item) => {
            if (item.value.length > 2)
              return item.value[2] > 0 ? upColor : downColor
            else
              return upColor
          }
        },
        // data: volumeData.value
      },
      {
        type: 'line',
        // nameLocation : 'middle',
        name: '均价',
        show: true,
        xAxisIndex: 2,
        yAxisIndex: 2,
        // nameGap: 30,
        scale: true,
        splitArea: {
          show: true
        },
        lineStyle: {
          width: 1
        },
        connectNulls: true,
        axisLabel: { show: true },
        axisLine: { show: false },
        axisTick: { show: true },
        splitLine: { show: false }
      },
      {
        type: 'line',
        // nameLocation : 'middle',
        name: '盈亏',
        show: true,
        xAxisIndex: 2,
        yAxisIndex: 3,
        // nameGap: 30,
        scale: true,
        splitArea: {
          show: true
        },
        lineStyle: {
          width: 1
        },
        connectNulls: true,
        axisLabel: { show: true },
        axisLine: { show: false },
        axisTick: { show: true },
        splitLine: { show: false }
      },
      {
        type: 'line',
        // nameLocation : 'middle',
        name: '市值',
        show: true,
        xAxisIndex: 2,
        yAxisIndex: 4,
        // nameGap: 30,
        scale: true,
        splitArea: {
          show: true
        },
        lineStyle: {
          width: 1
        },
        connectNulls: true,
        axisLabel: { show: true },
        axisLine: { show: false },
        axisTick: { show: true },
        splitLine: { show: false }
      },      
      {
        type: 'bar',
        name: '持有',
        show: true,
        xAxisIndex: 2,
        yAxisIndex: 5,        
        // nameGap: 30,
        scale: true,
        splitArea: {
          show: true
        },
        itemStyle: {
          color: quantityColor
        },
        axisLabel: { show: true },
        axisLine: { show: false },
        axisTick: { show: true },
        splitLine: { show: false }
      }
    ]  
  }
)

function makeMASeries() {
  for (const index in maItems) {
    chartOption.value.series.push({
      type: 'line',
      name: `ma-${maItems[index]}`,
      xAxisIndex: 0,
      yAxisIndex: 0,
      showSymbol: false,
      lineStyle: {
        width: 1
      },
      data: maData.value[index]
    })
  }
}


function setKLineData(data: HistoryData[]) {
  xData.value = data.map(item => item.日期)
  klineData.value = data.map(item => [item.开盘, item.收盘, item.最低, item.最高])
  volumeData.value = data.map(item => [item.日期, item.成交量, item.开盘 <= item.收盘 ? 1 : -1])

  const closeData = data.map(item => item.收盘)
  maData.value = []
  for (const ma of maItems) {
    maData.value.push(Calc.calcMAData(ma, closeData))
  }

  chartOption.value.xAxis[0].data = xData.value
  chartOption.value.xAxis[1].data = xData.value
  chartOption.value.xAxis[2].data = xData.value

  chartOption.value.series[0].data = klineData.value
  chartOption.value.series[1].data = volumeData.value

  makeMASeries()
}

function setTraceData(data: ProfitTraceItem[]) {
  // profitTraceData.value = calcProfitTraceData(data, historyData)
  
  priceAvgData.value = data.map(item => [item.date, item.price_avg])
  revenueData.value = data.map(item => [item.date, item.revenue])
  profitData.value = data.map(item => [item.date, item.profit])
  quantityData.value = data.map(item => [item.date, item.quantity])

  chartOption.value.series[2].data = priceAvgData.value
  chartOption.value.series[3].data = profitData.value
  chartOption.value.series[4].data = revenueData.value
  chartOption.value.series[5].data = quantityData.value
}

watch(
  () => props.historyData,
  (value) => {
    if (value) {
      setKLineData(value)
    }
})

watch(
  () => props.profitData,
  (value) => {
    if (value) {
      if(props.historyData) {
        setTraceData(value)
      }
    }
})

</script>
<template>
    <Echart :options="chartOption" class="my-4" ref="kline" :height="height" />
</template>
