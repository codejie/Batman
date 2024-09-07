<!--
KLine that support fetch data by code
-->
<script setup lang="ts">
import { ref, PropType, watch, unref } from 'vue'
import { Echart, EChartsOption } from '@/components/Echart'
import { DataParam, ReqParam, ShowParam } from '..';
import { apiHistory } from '@/api/data/wrap';

const DEFAULT_START: string = '2023-01-01'

const props = defineProps({
  reqParam: {
    type: Object as PropType<ReqParam>,
    required: false,
    default() {
      return {
        type: 1,
        code: '000001',
        start: '2023-01-01'
      }
    }
  },
  showParam: {
    type: Object as PropType<ShowParam>,
    required: false,
    default() {
      return {
        maLines: [],
        markLines: false,
        hideVolume: false,
        hideKLine: false
      }
    }
  }
})

const originData = ref<DataParam>([])

defineExpose({
  originData
})

let xData: string[] = []
let klineData: any[] = []
let volumeData: any[] = []

const upColor = '#ec0000'
const downColor = '#00da3c'

const options = ref<EChartsOption>({
  title: [],
  grid: [
    {
      left: '8%',
      right: '8%',
      height: '60%',
      top: '0%'
    },
    {
      left: '8%',
      right: '8%',
      bottom: '10%',
      height: '25%'
    }     
  ],
  legend: {
    bottom: 0,
    // orient: 'vertical',
    data: [],
    icon: 'circle'
  },
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
      // name: 'Value',
      nameLocation : 'middle',
      show: true,
      gridIndex: 0,
      position: 'left',
      nameGap: 30,
      // inverse: true
      scale: true,
      splitArea: {
        show: true
      }
    },
    {
      type: 'value',
      // name: 'Volume',
      nameLocation : 'middle',
      show: true,
      gridIndex: 1,
      position: 'left',
      nameGap: 30,
      // inverse: true
      scale: true,
      splitArea: {
        show: true
      },
      splitNumber: 8,
      axisLabel: { show: false },
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { show: false }
    }     
  ],
  series: [
    {
      name: 'KLine',
      type: 'candlestick',
      data: [],
      itemStyle: {
        color: upColor,
        color0: downColor,
        borderColor: undefined,
        borderColor0: undefined
      },
      xAxisIndex: 0,
      yAxisIndex: 0,
      markLine: {
        symbol: ['none', 'none'],
        data: []
      }
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
  }  
})

watch(
  () => props.reqParam,
  async () => {
    console.log(`type = ${props.reqParam.type}`)
    const ret = await apiHistory({
      code: props.reqParam.code,
      start: props.reqParam.start || DEFAULT_START,
      end: props.reqParam.end
    }, props.reqParam.type)
    originData.value = (ret.result as DataParam)
    updateData(unref(originData))
    updateOptions()
  }
)

watch(
  () => props.showParam,
  async () => {
    updateOptions()
  }
)

function updateData(data: DataParam) {
  xData = data.map(item => item.date)
  klineData = data.map(({open, close, low, high}) => ([open, close, low, high]))
  volumeData = data.map(item => [item.date, item.volume, item.open > item.close ? 1 : -1])
}

function updateOptions() {
  options.value.series = (options.value.series! as Array<any>).slice(0, 2)

  options.value.series![0].markLine.data = []
  options.value.legend!.data = []

  if (props.showParam.hideKLine) {
    options.value.series![0].itemStyle.color = '#777'
    options.value.series![0].itemStyle.color0 = '#777'
    // upColor = '#777'
    // downColor = '#777'
  } else {
    options.value.series![0].itemStyle.color = upColor
    options.value.series![0].itemStyle.color0 = downColor
  }

  if (props.showParam.markLines) {
    options.value.series![0].markLine.data.push({
      name: 'min',
      type: 'min',
      valueDim: 'close'
    })
    options.value.series![0].markLine.data.push({
      name: 'max',
      type: 'max',
      valueDim: 'close'
    })
  }

  if (props.showParam.hideVolume) {
    options.value.grid![0].height = '90%'
    options.value.grid![1].height = '0%'
  } else {
    options.value.grid![0].height = '60%'
    options.value.grid![1].height = '25%'    
  }

  options.value.xAxis![0].data = xData
  options.value.xAxis![1].data = xData
  options.value.series![0].data = klineData
  options.value.series![1].data = volumeData
  
  if (props.showParam.maLines.length > 0) {
    const closeData = klineData.map(item => item[1])
    for (const ma of props.showParam.maLines) {
      options.value.series!.push({
        name: `MA${ma}`,
        type: 'line',
        xAxisIndex: 0,
        yAxisIndex: 0,
        showSymbol: false,
        lineStyle: {
          width: 1
        },
        data: calcMAData(ma, closeData)
      })
      options.value.legend!.data.push(`MA${ma}`)
    }
  }
}

function calcMAData(ma: number, data: number[]) {
  var result: any[] = [];
  for (var i = 0, len = data.length; i < len; i++) {
    if (i < ma) {
      result.push('-')
      continue;
    }
    var sum = 0;
    for (var j = 0; j < ma; j++) {
      sum += +data[i - j]
    }
    result.push((sum / ma).toFixed(2))
  }
  return result
}

</script>
<template>
  <!-- <Echart v-if="param != undefined" :options="options" /> -->
  <Echart :options="options" />
</template>
