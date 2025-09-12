<script setup lang="ts">
import { Echart } from '@/components/Echart'
import type { EChartsOption } from 'echarts'
import { computed, PropType } from 'vue'
import type { SeriesDataItem } from './types'

const props = defineProps({
  mainTitle: {
    type: String,
    default: ''
  },
  height: {
    type: String,
    default: '600px'
  },
  xAxisData: {
    type: Array as PropType<string[]>,
    required: true
  },
  series: {
    type: Array as PropType<{ name: string; series: SeriesDataItem[] }[]>,
    required: true
  }
})

const option = computed((): EChartsOption => {
  const grid: any[] = []
  const xAxis: any[] = []
  const yAxis: any[] = []
  const series: any[] = []
  const title: any[] = []
  const numCharts = props.series.length
  const xAxisIndices = Array.from({ length: numCharts }, (_, k) => k)

  const dataZoom: any[] = [
    {
      type: 'inside',
      xAxisIndex: xAxisIndices,
      start: 0,
      end: 100
    },
    {
      show: true,
      xAxisIndex: xAxisIndices,
      type: 'slider',
      bottom: 10,
      start: 0,
      end: 100
    }
  ]

  if (numCharts === 0) {
    // Return a blank chart if there are no series
    return {}
  }

  const weights = [2, ...Array(numCharts > 1 ? numCharts - 1 : 0).fill(1)]
  const totalWeight = weights.reduce((a, b) => a + b, 0)

  let topMargin = 2
  if (props.mainTitle) {
    title.push({
      text: props.mainTitle,
      top: '0%',
      left: '0',
      textStyle: {
        fontWeight: 'bold',
        fontSize: 16
      }
    })
    topMargin = 5 // Increase top margin if there is a main title
  }

  const availableHeight = 85 // Use 85% of the container for charts and titles
  const totalChartHeight = availableHeight - topMargin

  let currentTop = topMargin

  props.series.forEach((chart, index) => {
    const chartWeight = weights[index]
    const singleChartAllocation = (totalChartHeight / totalWeight) * chartWeight

    const gridHeight = singleChartAllocation * 0.7
    const titleHeight = singleChartAllocation * 0.2

    const top = currentTop

    grid.push({
      left: '2%',
      right: '12%',
      top: `${top + titleHeight}%`,
      height: `${gridHeight}%`
    })

    title.push({
      text: chart.name,
      top: `${top}%`,
      left: '0',
      textStyle: {
        fontSize: 12,
        fontWeight: 'bold'
      }
    })

    xAxis.push({
      type: 'category',
      data: props.xAxisData,
      gridIndex: index,
      axisLabel: { show: index === numCharts - 1 },
      axisTick: { show: index === numCharts - 1 }
    })

    yAxis.push({
      scale: true,
      gridIndex: index,
      splitArea: { show: false }
    })

    chart.series.forEach((s) => {
      series.push({
        ...s,
        xAxisIndex: index,
        yAxisIndex: index
      })
    })
    currentTop += singleChartAllocation
  })

  return {
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
      }
    },
    axisPointer: {
      link: [{ xAxisIndex: 'all' }],
      label: {
        backgroundColor: '#777'
      }
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      data: props.series.flatMap((chart) => chart.series.map((s) => s.name))
    },
    grid,
    xAxis,
    yAxis,
    series,
    dataZoom,
    title
  }
})
</script>

<template>
  <Echart :options="option" :height="height" />
</template>
