<script setup lang="ts">
import { ref, PropType, watch, unref } from 'vue'
import { Echart, EChartsOption } from '@/components/Echart'
import { apiHistory } from '@/api/data/stock';
import { HistoryDataModel } from '@/api/data/stock/types';

export type DataParam = {
  code: string,
  start: string,
  end: string,
  period?: string,
  adjust?: string
}

export type ShowParam = {
  maLines: number[],
}

const props = defineProps({
  data: {
    type: Object as PropType<DataParam>,
    required: true
  },
  show: {
    type: Object as PropType<ShowParam>,
    required: false,
    default() {
      return {
        maLines: []
      }
    }
  }
})

const upColor = '#ec0000'
const downColor = '#00da3c'
const options = ref<EChartsOption>({
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
  legend: {
    left: 'true',
    orient: 'vertical',
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
      name: 'Value',
      nameLocation : 'middle',
      show: true,
      gridIndex: 0,
      position: 'left',
      nameGap: 30,
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
      nameGap: 30,
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
  }  
})

watch(
  () => props.data,
  async (value) => {
    if (value) {
      const ret = await apiHistory(unref(value)!)
      updateData(ret.result as HistoryDataModel[])
    }
  }
)

function updateData(data: HistoryDataModel[]) {
  const xData = data.map(item => item.date)
  options.value.xAxis![0].data = xData
  options.value.xAxis![1].data = xData
  options.value.series![0].data = data.map(({open, close, low, high}) => ([open, close, low, high]))
  options.value.series![1].data = data.map(item => [item.date, item.volume, item.open < item.close ? 1 : -1])

  options.value.series = options.value.series!.slice(0, 1)
  const closeData = data.map(({close}) => close)
  const ma = props.show.maLines;
  for (const d of ma) {
    makeMASeries(d, closeData)
  }
}

function makeMASeries(ma: number, data: number[]) {
  options.value.series!.push({
    name: `MA-${ma}`,
    type: 'line',
    xAxisIndex: 0,
    yAxisIndex: 0,
    showSymbol: false,
    lineStyle: {
      width: 1
    },
    data: calcMAData(ma, data)
  })
  options.value.legend!.data.push(`MA-${ma}`)
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
