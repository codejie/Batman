<script setup lang="ts">
import { ref, PropType, watchEffect } from 'vue'
import { Echart, EChartsOption } from '@/components/Echart'
import type { SeriesDataItem } from './types'

const props = defineProps({
  // 上方图表的系列数据
  topSeriesData: {
    type: Array as PropType<SeriesDataItem[]>,
    required: true
  },
  // 中间图表的系列数据
  middleSeriesData: {
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
    default: '600px' // 增加默认高度
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
  middleYAxisName: {
    type: String,
    default: ''
  },
  bottomYAxisName: {
    type: String,
    default: ''
  },
  // 新增：坐标系高度占比数组
  gridRatios: {
    type: Array as PropType<number[]>,
    default: () => [3, 1, 2] // 默认为3:1:2
  }
})

const options = ref<EChartsOption>({})

watchEffect(() => {
  // 1. 根据Ratios计算上中下grid的高度和位置
  const totalDrawHeight = 90 // 可供绘制的总高度百分比 (留出上下边距)
  const gap = 4 // grid之间的间距百分比
  const totalRatio = props.gridRatios.reduce((sum, ratio) => sum + ratio, 0)

  const topHeight = (totalDrawHeight - gap * 2) * (props.gridRatios[0] / totalRatio)
  const middleHeight = (totalDrawHeight - gap * 2) * (props.gridRatios[1] / totalRatio)
  const bottomHeight = (totalDrawHeight - gap * 2) * (props.gridRatios[2] / totalRatio)

  const topGridTop = 2 // 顶部边距
  const middleGridTop = topGridTop + topHeight + gap
  const bottomGridTop = middleGridTop + middleHeight + gap

  // 2. 合并图例和系列数据
  const legendData = [
    ...props.topSeriesData.map((s) => s.name),
    ...props.middleSeriesData.map((s) => s.name),
    ...props.bottomSeriesData.map((s) => s.name)
  ]

  const processSeries = (seriesData: SeriesDataItem[], xAxisIndex: number, yAxisIndex: number) => {
    return seriesData.map((s) => {
      const seriesItem = { ...s, xAxisIndex, yAxisIndex }
      if (s.type === 'line') {
        seriesItem.lineStyle = { ...s.lineStyle, width: 1 }
      }
      return seriesItem
    })
  }

  const series = [
    ...processSeries(props.topSeriesData, 0, 0),
    ...processSeries(props.middleSeriesData, 1, 1),
    ...processSeries(props.bottomSeriesData, 2, 2)
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
      },
      formatter: (params) => {
        const topSeriesCount = props.topSeriesData.length
        const middleSeriesCount = props.middleSeriesData.length

        const topParams = params.filter((p) => p.seriesIndex < topSeriesCount)
        const middleParams = params.filter(
          (p) =>
            p.seriesIndex >= topSeriesCount && p.seriesIndex < topSeriesCount + middleSeriesCount
        )
        const bottomParams = params.filter(
          (p) => p.seriesIndex >= topSeriesCount + middleSeriesCount
        )

        let tooltipContent = `${params[0].axisValueLabel}<br/>`

        const formatParam = (param) => {
          const seriesName = param.seriesName
          const value = param.value
          const marker = param.marker
          let formattedValue = ''

          if (Array.isArray(value)) {
            formattedValue = `O:${value[0].toFixed(2)} C:${value[1].toFixed(2)} L:${value[2].toFixed(2)} H:${value[3].toFixed(2)}`
          } else if (typeof value === 'number') {
            formattedValue = value.toFixed(2)
          } else {
            formattedValue = value
          }
          return `${marker} ${seriesName}: <b>${formattedValue}</b><br/>`
        }

        if (topParams.length > 0) {
          topParams.forEach((param) => {
            tooltipContent += formatParam(param)
          })
        }

        if (middleParams.length > 0) {
          tooltipContent += '<hr style="margin: 5px 0; border-style: dashed;"/>'
          middleParams.forEach((param) => {
            tooltipContent += formatParam(param)
          })
        }

        if (bottomParams.length > 0) {
          tooltipContent += '<hr style="margin: 5px 0; border-style: dashed;"/>'
          bottomParams.forEach((param) => {
            tooltipContent += formatParam(param)
          })
        }

        return tooltipContent
      }
    },
    legend: {
      show: props.showLegend,
      data: legendData,
      top: `${bottomGridTop + bottomHeight + 2}%`, // Adjust this
      icon: 'circle'
    },
    axisPointer: {
      link: [{ xAxisIndex: 'all' }],
      label: {
        backgroundColor: '#777'
      }
    },
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
        top: `${middleGridTop}%`,
        height: `${middleHeight}%`
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
        axisLabel: { show: true },
        name: props.xAxisName,
        nameLocation: 'center',
        nameGap: 30
      },
      {
        type: 'category',
        data: props.xAxisData,
        gridIndex: 1,
        axisLabel: { show: false }
      },
      {
        type: 'category',
        data: props.xAxisData,
        gridIndex: 2,
        axisLabel: { show: false }
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
        name: props.middleYAxisName,
        nameLocation: 'center',
        nameGap: 40,
        scale: true,
        splitArea: { show: true },
        axisLine: { show: true, lineStyle: { color: '#8392A5' } }
      },
      {
        type: 'value',
        gridIndex: 2,
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
