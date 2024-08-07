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
  markLines: boolean
}

const props = defineProps({
  data: {
    type: Object as PropType<DataParam>,
    required: false
  },
  show: {
    type: Object as PropType<ShowParam>,
    required: false,
    default() {
      return {
        maLines: [],
        markLines: false
      }
    }
  }
})

const upColor = '#ec0000'
const downColor = '#00da3c'

const xData = ref<string[]>(
  [
    "2023-06-01",
    "2023-06-02",
    "2023-06-05",
    "2023-06-06",
    "2023-06-07",
    "2023-06-08",
    "2023-06-09",
    "2023-06-12",
    "2023-06-13",
    "2023-06-14",
    "2023-06-15",
    "2023-06-16",
    "2023-06-19",
    "2023-06-20",
    "2023-06-21",
    "2023-06-26",
    "2023-06-27",
    "2023-06-28",
    "2023-06-29",
    "2023-06-30",
    "2023-07-03",
    "2023-07-04",
    "2023-07-05",
    "2023-07-06",
    "2023-07-07",
    "2023-07-10",
    "2023-07-11",
    "2023-07-12",
    "2023-07-13",
    "2023-07-14",
    "2023-07-17",
    "2023-07-18",
    "2023-07-19",
    "2023-07-20",
    "2023-07-21",
    "2023-07-24",
    "2023-07-25",
    "2023-07-26",
    "2023-07-27",
    "2023-07-28",
    "2023-07-31",
    "2023-08-01",
    "2023-08-02",
    "2023-08-03",
    "2023-08-04",
    "2023-08-07",
    "2023-08-08",
    "2023-08-09",
    "2023-08-10",
    "2023-08-11",
    "2023-08-14",
    "2023-08-15",
    "2023-08-16",
    "2023-08-17",
    "2023-08-18",
    "2023-08-21",
    "2023-08-22",
    "2023-08-23",
    "2023-08-24",
    "2023-08-25",
    "2023-08-28",
    "2023-08-29",
    "2023-08-30",
    "2023-08-31",
    "2023-09-01",
    "2023-09-04",
    "2023-09-05",
    "2023-09-06",
    "2023-09-07",
    "2023-09-08",
    "2023-09-11",
    "2023-09-12",
    "2023-09-13",
    "2023-09-14",
    "2023-09-15",
    "2023-09-18",
    "2023-09-19",
    "2023-09-20",
    "2023-09-21",
    "2023-09-22",
    "2023-09-25",
    "2023-09-26",
    "2023-09-27",
    "2023-09-28"
]  
)
const yData = ref<any[]>([
    [
        18.87,
        19.97,
        18.67,
        20.42
    ],
    [
        19.96,
        19.73,
        19.66,
        20.17
    ],
    [
        19.71,
        20.02,
        19.44,
        20.42
    ],
    [
        19.95,
        19.13,
        19.01,
        20.01
    ],
    [
        19.13,
        18.97,
        18.79,
        19.33
    ],
    [
        18.91,
        18.59,
        18.29,
        18.93
    ],
    [
        18.75,
        18.06,
        17.63,
        18.86
    ],
    [
        18.3,
        18.15,
        17.83,
        18.36
    ],
    [
        18.16,
        19.39,
        17.94,
        19.55
    ],
    [
        19.43,
        19.76,
        19.2,
        20.3
    ],
    [
        19.47,
        18.75,
        18.6,
        19.64
    ],
    [
        18.66,
        20.69,
        18.41,
        20.69
    ],
    [
        21.36,
        22.46,
        20.71,
        22.72
    ],
    [
        21.92,
        23.08,
        21.77,
        23.44
    ],
    [
        22.71,
        21.41,
        21.41,
        22.71
    ],
    [
        21.11,
        20.44,
        20.22,
        21.82
    ],
    [
        20.34,
        20.36,
        20.02,
        20.59
    ],
    [
        20.16,
        18.51,
        18.26,
        20.17
    ],
    [
        18.88,
        19.04,
        18.81,
        19.46
    ],
    [
        18.77,
        19.06,
        18.45,
        19.35
    ],
    [
        19.11,
        19.26,
        18.88,
        19.51
    ],
    [
        19.06,
        20.84,
        19.03,
        21.16
    ],
    [
        21.29,
        20.75,
        20.61,
        21.64
    ],
    [
        20.63,
        21,
        20.54,
        21.74
    ],
    [
        20.82,
        20.15,
        19.56,
        20.86
    ],
    [
        20.42,
        20.02,
        19.78,
        20.49
    ],
    [
        19.93,
        20.98,
        19.88,
        21.32
    ],
    [
        21.51,
        20.99,
        20.93,
        21.79
    ],
    [
        20.83,
        21.81,
        20.67,
        22.09
    ],
    [
        21.71,
        21.3,
        21.23,
        21.85
    ],
    [
        21.17,
        21.69,
        20.93,
        22.11
    ],
    [
        21.51,
        21.21,
        21.01,
        21.54
    ],
    [
        21.21,
        21.33,
        21,
        21.5
    ],
    [
        21.37,
        20.16,
        20.16,
        21.4
    ],
    [
        20.19,
        19.87,
        19.66,
        20.29
    ],
    [
        19.89,
        20.16,
        19.89,
        20.76
    ],
    [
        20.39,
        20.46,
        20,
        20.81
    ],
    [
        20.43,
        19.68,
        19.52,
        20.43
    ],
    [
        19.62,
        19.36,
        19.3,
        19.79
    ],
    [
        19.27,
        19.77,
        19.21,
        19.87
    ],
    [
        19.76,
        21.26,
        19.46,
        21.81
    ],
    [
        21.06,
        21.04,
        20.84,
        21.25
    ],
    [
        20.91,
        20.9,
        20.63,
        21.04
    ],
    [
        20.71,
        20.29,
        19.96,
        20.96
    ],
    [
        20.29,
        21.6,
        20.29,
        21.86
    ],
    [
        21.6,
        21.64,
        21.28,
        22.07
    ],
    [
        21.49,
        21.21,
        21.15,
        21.66
    ],
    [
        21.21,
        20.44,
        20.33,
        21.43
    ],
    [
        20.42,
        20.44,
        20.19,
        20.59
    ],
    [
        20.37,
        19.75,
        19.75,
        20.54
    ],
    [
        19.74,
        20.08,
        19.4,
        20.11
    ],
    [
        20.02,
        19.73,
        19.46,
        20.36
    ],
    [
        19.59,
        18.74,
        18.58,
        19.65
    ],
    [
        18.67,
        19.11,
        18.52,
        19.19
    ],
    [
        19.02,
        18.93,
        18.9,
        19.56
    ],
    [
        18.87,
        19.2,
        18.76,
        19.65
    ],
    [
        19.36,
        20.01,
        18.96,
        20.02
    ],
    [
        19.76,
        19.21,
        19.13,
        19.91
    ],
    [
        19.46,
        19.39,
        19.26,
        19.87
    ],
    [
        19.11,
        18.71,
        17.99,
        19.11
    ],
    [
        20.11,
        19.52,
        19.36,
        20.13
    ],
    [
        19.5,
        20.72,
        19.38,
        20.93
    ],
    [
        20.81,
        20.74,
        20.51,
        20.93
    ],
    [
        20.76,
        20.89,
        20.54,
        21.41
    ],
    [
        20.86,
        20.83,
        20.67,
        21.06
    ],
    [
        20.96,
        21.03,
        20.71,
        21.19
    ],
    [
        20.89,
        20.64,
        20.61,
        21.25
    ],
    [
        20.5,
        20.54,
        20.08,
        20.8
    ],
    [
        20.37,
        19.96,
        19.93,
        20.68
    ],
    [
        19.91,
        20.06,
        19.59,
        20.46
    ],
    [
        19.95,
        20.48,
        19.81,
        20.83
    ],
    [
        20.36,
        20.57,
        20.21,
        20.72
    ],
    [
        20.32,
        19.84,
        19.73,
        20.51
    ],
    [
        19.82,
        19.71,
        19.53,
        19.95
    ],
    [
        19.81,
        19.87,
        19.27,
        19.87
    ],
    [
        19.51,
        19.43,
        19.28,
        19.75
    ],
    [
        19.36,
        19.11,
        19.06,
        19.48
    ],
    [
        19.15,
        19.27,
        19.12,
        19.52
    ],
    [
        19.2,
        19.11,
        19.01,
        19.56
    ],
    [
        19.03,
        20.24,
        18.89,
        20.35
    ],
    [
        20.17,
        19.91,
        19.89,
        20.36
    ],
    [
        21.02,
        21.97,
        20.61,
        21.97
    ],
    [
        21.98,
        22.2,
        21.67,
        22.48
    ],
    [
        22.02,
        21.58,
        21.44,
        22.16
    ]
])

function calculateMA(dayCount) {
  var result: any[] = [];
  for (var i = 0, len = yData.value.length; i < len; i++) {
    if (i < dayCount) {
      result.push('-');
      continue;
    }
    var sum = 0;
    for (var j = 0; j < dayCount; j++) {
      sum += +yData.value[i - j][1];
    }
    result.push(sum / dayCount);
  }
  return result;
}

const options = ref<EChartsOption>({
  title: {
    text: '上证指数',
    left: 0
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    }
  },
  legend: {
    data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
  },
  grid: {
    left: '10%',
    right: '10%',
    bottom: '15%'
  },
  xAxis: {
    type: 'category',
    data: xData.value,
    boundaryGap: false,
    axisLine: { onZero: false },
    splitLine: { show: true },
    // min: 'dataMin',
    // max: 'dataMax'
  },
  yAxis: {
    scale: true,
    splitArea: {
      show: true
    }
  },
  // dataZoom: [
  //   {
  //     type: 'inside',
  //     start: 50,
  //     end: 100
  //   },
  //   {
  //     show: true,
  //     type: 'slider',
  //     top: '90%',
  //     start: 50,
  //     end: 100
  //   }
  // ],
  series: [
    {
      name: '日K',
      type: 'candlestick',
      data: yData.value,
      itemStyle: {
        color: upColor,
        color0: downColor
      },
      markLine: {
        symbol: ['none', 'none'],
        data: [
          {
            name: 'min line on close',
            type: 'min',
            valueDim: 'close'
          }
        ]
      }
    },
    {
      name: 'MA5',
      type: 'line',
      data: calculateMA(5),
      smooth: true,
      lineStyle: {
        opacity: 0.5
      }
    },
    {
      name: 'MA10',
      type: 'line',
      data: calculateMA(10),
      smooth: true,
      lineStyle: {
        opacity: 0.5
      }
    },
    {
      name: 'MA20',
      type: 'line',
      data: calculateMA(20),
      smooth: true,
      lineStyle: {
        opacity: 0.5
      }
    },
    {
      name: 'MA30',
      type: 'line',
      data: calculateMA(30),
      smooth: true,
      lineStyle: {
        opacity: 0.5
      }
    }
  ]  
})

// watch(
//   () => props.data,
//   async (value) => {
//     if (value) {
//       const ret = await apiHistory(unref(value)!)
//       updateData(ret.result as HistoryDataModel[])
//     }
//   }
// )

// function updateData(data: HistoryDataModel[]) {
//   xData.value = data.map(item => item.date)
//   console.log(xData.value)
//   yData.value = data.map(({open, close, low, high}) => ([open, close, low, high]))
//   console.log(yData.value)
// }


</script>
<template>
  <!-- <Echart v-if="param != undefined" :options="options" /> -->
  <Echart :options="options" />
</template>
