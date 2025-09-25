<script setup lang="ts">
import { ref, PropType, watchEffect } from 'vue'
import { Echart, EChartsOption } from '@/components/Echart'
import type { SeriesDataItem } from './types'

const props = defineProps({
  // 接收图表系列的配置数组
  seriesData: {
    type: Array as PropType<SeriesDataItem[]>,
    required: true,
    default: () => []
  },
  // X轴的类目数据
  xAxisData: {
    type: Array as PropType<string[]>,
    required: true,
    default: () => []
  },
  // 可选的图表标题
  title: {
    type: String,
    default: ''
  },
  // 图表高度
  height: {
    type: String,
    default: '400px'
  },
  // X轴名称
  xAxisName: {
    type: String,
    default: ''
  },
  // Y轴名称
  yAxisName: {
    type: String,
    default: ''
  },
  // 控制图例显示
  showLegend: {
    type: Boolean,
    default: true
  }
})

const options = ref<EChartsOption>({})

// 使用 watchEffect 来响应 props 的变化，并更新 echarts 配置
watchEffect(() => {
  options.value = {
    // 图表标题
    title: {
      text: props.title,
      left: 'center'
    },
    // 提示框
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: (params) => {
        let tooltipContent = `${params[0].axisValueLabel}<br/>`
        params.forEach((param) => {
          const seriesName = param.seriesName
          const value = param.value
          const marker = param.marker

          let formattedValue = ''
          if (typeof value === 'number') {
            formattedValue = value.toFixed(2)
          } else if (Array.isArray(value)) {
            // Handle Candlestick data [open, close, lowest, highest]
            formattedValue = value.map((v) => v.toFixed(2)).join(', ')
          } else {
            formattedValue = value
          }

          tooltipContent += `${marker} ${seriesName}: <b>${formattedValue}</b><br/>`
        })
        return tooltipContent
      }
    },
    // 图例，根据传入的 seriesData 动态生成
    legend: {
      show: props.showLegend,
      data: props.seriesData.map((s) => s.name),
      bottom: 0,
      icon: 'circle'
    },
    // 单一的网格（坐标系）
    grid: {
      left: '5%',
      right: '5%',
      bottom: '10%',
      top: '5%',
      containLabel: true
    },
    // X轴
    xAxis: {
      type: 'category',
      data: props.xAxisData,
      name: props.xAxisName,
      nameLocation: 'center',
      nameGap: 30 // 调整名称与轴线的距离
    },
    // Y轴
    yAxis: {
      type: 'value',
      scale: true, // 自动缩放
      splitArea: {
        show: true
      },
      name: props.yAxisName,
      nameLocation: 'center',
      nameGap: 40, // 调整名称与轴线的距离
      axisLine: {
        show: true,
        lineStyle: {
          color: '#8392A5' // 设置一个中性色
        }
      }
    },
    // 核心：根据 props.seriesData 动态生成图表系列
    series: props.seriesData.map((item) => {
      const seriesItem = { ...item }
      if (item.type === 'line') {
        seriesItem.lineStyle = { ...item.lineStyle, width: 1 }
      }
      return seriesItem
    }),
    // 用于K线图和成交量柱状图的颜色区分
    visualMap: {
      show: false,
      seriesIndex: props.seriesData.findIndex((s) => s.type === 'bar'), // 作用于柱状图
      dimension: 2,
      pieces: [
        { value: 1, color: '#ec0000' }, // 红色
        { value: -1, color: '#00da3c' } // 绿色
      ]
    },
    axisPointer: {
      label: {
        backgroundColor: '#777'
      }
    }
  }
})
</script>

<template>
  <Echart :options="options" :height="height" />
</template>
