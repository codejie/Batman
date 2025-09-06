<script setup lang="ts">
import { ref, PropType, watchEffect } from 'vue'
import { Echart, EChartsOption } from '@/components/Echart'
import type { SeriesDataItem } from '.'

const props = defineProps({
  // 上方图表的系列数据
  topSeriesData: {
    type: Array as PropType<SeriesDataItem[]>,
    required: true
  },
  // 下方图表的系列数据
  bottomSeriesData: {
    type: Array as PropType<SeriesDataItem[]>,
    required: true
  },
  // 共享的X轴类目数据
  xAxisData: {
    type: Array as PropType<string[]>,
    required: true
  },
  // --- 可选通用配置 ---
  title: {
    type: String,
    default: ''
  },
  height: {
    type: String,
    default: '500px'
  },
  showLegend: {
    type: Boolean,
    default: true
  },
  // --- 可选坐标轴名称 ---
  xAxisName: {
    type: String,
    default: ''
  },
  topYAxisName: {
    type: String,
    default: ''
  },
  bottomYAxisName: {
    type: String,
    default: ''
  },
  // 新增：坐标系高度占比
  gridRatio: {
    type: Number,
    default: 2 // 默认为2:1
  }
})

const options = ref<EChartsOption>({})

watchEffect(() => {
  // 1. 根据Ratio计算上下grid的高度和位置
  const totalDrawHeight = 78 // 可供绘制的总高度百分比 (留出上下边距)
  const gap = 12 // 上下grid的间距百分比
  const topHeight = (totalDrawHeight - gap) * (props.gridRatio / (props.gridRatio + 1))
  const bottomHeight = (totalDrawHeight - gap) * (1 / (props.gridRatio + 1))
  const topGridTop = 8 // 顶部边距
  const bottomGridTop = topGridTop + topHeight + gap

  // 2. 合并图例和系列数据
  const legendData = [
    ...props.topSeriesData.map((s) => s.name),
    ...props.bottomSeriesData.map((s) => s.name)
  ]
  const series = [
    ...props.topSeriesData.map((s) => ({ ...s, xAxisIndex: 0, yAxisIndex: 0 })),
    ...props.bottomSeriesData.map((s) => ({ ...s, xAxisIndex: 1, yAxisIndex: 1 }))
  ]

  // 3. 生成ECharts配置
  options.value = {
    title: {
      text: props.title,
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      show: props.showLegend,
      data: legendData,
      bottom: 0,
      icon: 'circle'
    },
    axisPointer: {
      link: [{ xAxisIndex: 'all' }],
      label: {
        backgroundColor: '#777'
      }
    },
    // 使用计算出的grid位置
    grid: [
      {
        left: '8%',
        right: '5%',
        top: `${topGridTop}%`,
        height: `${topHeight}%`
      },
      {
        left: '8%',
        right: '5%',
        top: `${bottomGridTop}%`,
        height: `${bottomHeight}%`
      }
    ],
    xAxis: [
      {
        type: 'category',
        data: props.xAxisData,
        gridIndex: 0,
        axisLabel: { show: false }
      },
      {
        type: 'category',
        data: props.xAxisData,
        gridIndex: 1,
        name: props.xAxisName,
        nameLocation: 'center',
        nameGap: 30
      }
    ],
    yAxis: [
      {
        type: 'value',
        gridIndex: 0,
        name: props.topYAxisName,
        nameLocation: 'center',
        nameGap: 40,
        scale: true,
        splitArea: { show: true },
        axisLine: { show: true, lineStyle: { color: '#8392A5' } }
      },
      {
        type: 'value',
        gridIndex: 1,
        name: props.bottomYAxisName,
        nameLocation: 'center',
        nameGap: 40,
        scale: true,
        splitArea: { show: true },
        axisLine: { show: true, lineStyle: { color: '#8392A5' } }
      }
    ],
    series: series
  }
})
</script>

<template>
  <Echart :options="options" :height="height" />
</template>