<script setup lang="ts">
import { ref } from 'vue'
import { Echart } from '@/components/Echart'
import { propTypes } from '@/utils/propTypes'

const props = defineProps({
  upColor: propTypes.string.def('#ec0000'),
  downColor: propTypes.string.def('#00da3c'),
  height: propTypes.oneOfType([Number, String]).def('500px'),
  width: propTypes.oneOfType([Number, String]).def('100%'),
  showLegend: propTypes.bool.def(true),
  theme: propTypes.string.def('light')
})

const options = ref<any>({
  title: [],
  grid: [],
  xAxis: [],
  yAxis: [],
  series: [],
  legend: {
    bottom: '0%',
    icon: 'circle',
    data: [],
    show: props.showLegend
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
    }
  },
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
  dataZoom: []
})

/**
 * Reset chart options to initial state
 */
function reset() {
  options.value = {
    title: [],
    grid: [],
    xAxis: [],
    yAxis: [],
    series: [],
    legend: {
      bottom: '0%',
      icon: 'circle',
      data: [],
      show: props.showLegend
    } as any,
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
      link: [
        {
          xAxisIndex: 'all'
        }
      ],
      label: {
        backgroundColor: '#777'
      }
    },
    dataZoom: []
  }
}

/**
 * Add a grid to the chart
 */
function addGrid(config: {
  id?: number | string
  left?: number | string
  top?: number | string
  right?: number | string
  bottom?: number | string
  width?: number | string
  height?: number | string
}) {
  if (!options.value.grid) options.value.grid = []
  if (Array.isArray(options.value.grid)) {
    options.value.grid.push({
      ...config
    })
  }
}

/**
 * Legacy support for addGrid with positional arguments
 */
function addGridLegacy(
  id: number,
  left: number | string,
  top: number | string,
  right: number | string,
  bottom: number | string,
  width?: number | string,
  height?: number | string
) {
  addGrid({ id, left, top, right, bottom, width, height })
}

/**
 * Link axes for crosshair and zoom synchronization
 */
function addAxisPointer(grids: number[] | 'all') {
  options.value.axisPointer = {
    link: [
      {
        xAxisIndex: grids
      }
    ],
    label: {
      backgroundColor: '#777'
    }
  }
}

/**
 * Add X and Y axes to a specific grid
 */
function addAxis(gridIndex: number, xData: any[], showLabel: boolean = true, scale: boolean = true) {
  if (!options.value.xAxis) options.value.xAxis = []
  if (!options.value.yAxis) options.value.yAxis = []

  if (Array.isArray(options.value.xAxis)) {
    options.value.xAxis.push({
      type: 'category',
      gridIndex: gridIndex,
      data: xData,
      boundaryGap: false,
      axisLine: { onZero: false },
      axisTick: { show: true },
      splitLine: { show: false },
      axisLabel: { show: showLabel }
    } as any)
  }

  if (Array.isArray(options.value.yAxis)) {
    options.value.yAxis.push({
      type: 'value',
      gridIndex: gridIndex,
      scale: scale, // Allow disabling scale for indicators like MACD
      splitArea: {
        show: true
      },
      splitNumber: 8,
      axisLabel: { show: showLabel },
      axisLine: { show: showLabel },
      axisTick: { show: showLabel },
      splitLine: { show: false }
    } as any)
  }
}

/**
 * Add a candlestick (K-Line) series
 */
function addKLine(
  gridIndex: number,
  name: string,
  data: any[],
  config: {
    markLine?: boolean
    legend?: boolean
    itemStyle?: any
  } = { markLine: true, legend: true }
) {
  const klineSer: any = {
    name: name,
    type: 'candlestick',
    xAxisIndex: gridIndex,
    yAxisIndex: gridIndex,
    itemStyle: config.itemStyle || {
      color: props.upColor,
      color0: props.downColor,
      borderColor: props.upColor,
      borderColor0: props.downColor
    },
    data: data
  }

  if (config.markLine) {
    klineSer.markLine = {
      symbol: ['none', 'none'],
      data: [
        { name: 'min', type: 'min', valueDim: 'close' },
        { name: 'max', type: 'max', valueDim: 'close' }
      ]
    }
  }

  if (!options.value.series) options.value.series = []
  if (Array.isArray(options.value.series)) {
    options.value.series.push(klineSer)
  }

  if (config.legend) {
    addToLegend(name)
  }
}

/**
 * Add a line series
 */
function addLine(
  gridIndex: number,
  name: string,
  data: any[],
  config: {
    legend?: boolean
    smooth?: boolean
    showSymbol?: boolean
    lineStyle?: any
  } = { legend: true, smooth: false, showSymbol: false }
) {
  const lineSer: any = {
    name: name,
    type: 'line',
    xAxisIndex: gridIndex,
    yAxisIndex: gridIndex,
    showSymbol: !!config.showSymbol,
    smooth: !!config.smooth,
    lineStyle: config.lineStyle || { width: 1 },
    data: data
  }

  if (!options.value.series) options.value.series = []
  if (Array.isArray(options.value.series)) {
    options.value.series.push(lineSer)
  }

  if (config.legend) {
    addToLegend(name)
  }
}

/**
 * Add a bar series
 */
function addBar(
  gridIndex: number,
  name: string,
  data: any[],
  config: {
    legend?: boolean
    itemStyle?: any
  } = { legend: true }
) {
  const barSer: any = {
    name: name,
    type: 'bar',
    xAxisIndex: gridIndex,
    yAxisIndex: gridIndex,
    itemStyle: config.itemStyle || {
      color: (params: any) => {
        // Highlighting positive/negative columns
        const data = params.value || params.data
        if (data && Array.isArray(data) && data.length > 2) {
          return data[2] > 0 ? props.upColor : props.downColor
        }
        return props.upColor
      }
    },
    data: data
  }

  if (!options.value.series) options.value.series = []
  if (Array.isArray(options.value.series)) {
    options.value.series.push(barSer)
  }

  if (config.legend) {
    addToLegend(name)
  }
}

/**
 * Add a step line series
 */
function addStepLine(
  gridIndex: number,
  name: string,
  data: any[],
  step: 'start' | 'middle' | 'end' = 'end',
  legend: boolean = true
) {
  const lineSer: any = {
    name: name,
    type: 'line',
    step: step,
    xAxisIndex: gridIndex,
    yAxisIndex: gridIndex,
    showSymbol: false,
    lineStyle: { width: 1 },
    data: data
  }

  if (!options.value.series) options.value.series = []
  if (Array.isArray(options.value.series)) {
    options.value.series.push(lineSer)
  }

  if (legend) {
    addToLegend(name)
  }
}

/**
 * Add DataZoom component
 */
function addDataZoom(config: any[] = []) {
  options.value.dataZoom = config.length
    ? config
    : [
        {
          type: 'inside',
          xAxisIndex: [0], // Only zoom the top chart for better control
          start: 0,
          end: 100
        }
      ]
}

/**
 * Helper to add name to legend
 */
function addToLegend(name: string) {
  const legend = options.value.legend as any
  if (!legend || !legend.data) return
  if (Array.isArray(legend.data)) {
    if (!legend.data.includes(name)) {
      legend.data.push(name)
    }
  }
}

/**
 * Remove series and legend items
 * mode: 0 - exact, 1 - wildcard (includes), 2 - prefix, 3 - suffix
 */
function remove(name: string, mode: number = 0) {
  if (!options.value.series) return

  let predicate: (item: string) => boolean
  let seriesPredicate: (item: any) => boolean

  switch (mode) {
    case 1: // wildcard
      predicate = (item) => !item.includes(name)
      seriesPredicate = (item) => !item.name?.includes(name)
      break
    case 2: // prefix
      predicate = (item) => !item.startsWith(name)
      seriesPredicate = (item) => !item.name?.startsWith(name)
      break
    case 3: // suffix
      predicate = (item) => !item.endsWith(name)
      seriesPredicate = (item) => !item.name?.endsWith(name)
      break
    case 0:
    default:
      predicate = (item) => item !== name
      seriesPredicate = (item) => item.name !== name
  }

  const legend = options.value.legend as any
  if (legend && Array.isArray(legend.data)) {
    legend.data = legend.data.filter(predicate)
  }

  if (Array.isArray(options.value.series)) {
    options.value.series = options.value.series.filter(seriesPredicate)
  }
}

defineExpose({
  reset,
  addGrid: addGridLegacy,
  addGridNew: addGrid,
  addAxisPointer,
  addAxis,
  addKLine,
  addLine,
  addBar,
  addStepLine,
  addDataZoom,
  remove,
  options // Expose options for direct manipulation if needed
})
</script>

<template>
  <Echart :options="options" :height="height" :width="width" />
</template>
