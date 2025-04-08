<script setup lang="ts">
import { ref } from 'vue';
import { Echart, EChartsOption } from '@/components/Echart';
import { XAXisOption } from 'echarts/types/dist/shared';

defineProps({
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

function makeKLineOption(grid: number, yAxis: number, name: string, data: any[]) {
  return {
    name: name,
    type: 'candlestick',
    itemStyle: {
      color: upColor,
      color0: downColor
    },
    xAxisIndex: grid,
    yAxisIndex: yAxis,
    markLine: {
      symbol: ['none', 'none'],
      data: [] as any[]
    },
    data: data
  }
}

function makeMarkLine(min: boolean) {
  return {
    name: min ? 'min' : 'max',
    type: min ? 'min' : 'max',
    valueDim: 'close'
  }  
}

function makeLineOption(grid: number, yAxis: number, name: string, data: any[]) {
  return {
    name: name,
    type: 'line',
    xAxisIndex: grid,
    yAxisIndex: yAxis,
    showSymbol: false,
    lineStyle: {
      width: 1
    },
    // itemStyle: {
    //   color: '#ec0000'
    // },
    data: data    
  }
}

function makeBarOption(grid: number, yAxis: number, name: string, data: any[]) {
  return {
    name: name,
    type: 'bar',
    xAxisIndex: grid,
    yAxisIndex: yAxis,
    showSymbol: false,
    itemStyle: {
      color: (item) => {
        if (item.length > 2)
          return item.[2] > 0 ? upColor : downColor
        else
          return upColor
      }
    },
    data: data
  }
}

function makeStepLineOption(grid: number, yAxis: number, name: string, data: any[], step: string = 'end') {
  return {
    name: name,
    type: 'line',
    step: step,
    xAxisIndex: grid,
    yAxisIndex: yAxis,
    showSymbol: false,
    lineStyle: {
      width: 1
    },
    // itemStyle: {
    //   color: '#ec0000'
    // },
    data: data    
  }
}

let options: EChartsOption = {}
//   title: [],
//   grid: [],
//   xAxis: [],
//   yAxis: [],
//   series: [],
//   legend: {
//     bottom: '0%',
//     icon: 'circle',
//     data: []
//   }
// }

function reset() { 
  options = {
    title: [],
    grid: [],
    xAxis: [],
    yAxis: [],
    series: [],
    legend: {
      bottom: '-2%',
      icon: 'circle',
      data: []
    }
  }
}

function addGrid(id: number, left: number | string, top: number | string, right: number | string, bottom: number | string, width?: number | string, height?: number | string) {
  (options.grid as any[]).push({
    id,
    left,
    top,
    right,
    bottom,
    width,
    height
  })
}

function addAxisPointer(grids: number[]) {
  options['axisPointer'] = {
    link: [
      {
        xAxisIndex: grids
      }
    ],
    label: {
      backgroundColor: '#777'
    }    
  }
  options['tooltip'] = {
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
  }
}

function addAxis(grid: number, xData: number[] | string[], yPosition: string = 'left', showTick: boolean = true): number {
  if (!options.xAxis) {
    options.xAxis = []
  }
  (options.xAxis as XAXisOption[]).push({
    type: 'category',
    gridIndex: grid,
    data: xData,
    boundaryGap: false,
    axisLine: { onZero: true },
    axisTick: { show: true },
    splitLine: { show: false },
    axisLabel: { show: showTick },    
  })
  (options.yAxis as []).push({
    type: 'value',
    // nameLocation : 'middle',
    show: true,
    gridIndex: grid,
    position: yPosition,
    nameGap: 30,
    scale: true,
    splitArea: {
      show: true
    },
    splitNumber: 8,
    axisLabel: { show: showTick },
    axisLine: { show: showTick },
    axisTick: { show: showTick },
    splitLine: { show: false }       
  })
  return (options.yAxis as []).length - 1
}

// function addAxis(grid: number, xdata: number[] | string[], showTick: boolean = true, yPosition: string = "left") {
//   options.xAxis!.push({
//     type: 'category',
//     gridIndex: grid,
//     data: xdata,
//     boundaryGap: false,
//     axisLine: { onZero: true },
//     axisTick: { show: true },
//     splitLine: { show: false },
//     axisLabel: { show: showTick },    
//   })
//   options.yAxis!.push({
//     type: 'value',
//     // nameLocation : 'middle',
//     show: true,
//     gridIndex: grid,
//     position: yPosition,
//     nameGap: 30,
//     scale: true,
//     splitArea: {
//       show: true
//     },
//     splitNumber: 8,
//     axisLabel: { show: showTick },
//     axisLine: { show: showTick },
//     axisTick: { show: showTick },
//     splitLine: { show: false }       
//   })  
// }

function addKLine(grid: number, yAxis: number, name: string, data: any[], markLine: boolean = true, legend: boolean = false) {
  const klineOpt = makeKLineOption(grid, yAxis, name, data)
  if (markLine) {
    klineOpt.markLine.data.push(makeMarkLine(true))
    klineOpt.markLine.data.push(makeMarkLine(false))
  }
  options.series!.push(klineOpt)
  if (legend) {
    options.legend!.data.push(name)
  }
}

function addLine(grid: number, yAxis: number, name: string, data: number[], legend: boolean = true) {
  const lineOpt = makeLineOption(grid, yAxis, name, data, yAxis)
  options.series!.push(lineOpt)
  if (legend) {
    options.legend!.data.push(name)
  }  
}

function addBar(grid: number, yAxis: number, name: string, data: number[], legend: boolean = true) {
  const barOpt = makeBarOption(grid, yAxis, name, data)
  options.series!.push(barOpt)
  if (legend) {
    options.legend!.data.push(name)
  }  
}

function addStepLine(grid: number, yAxis: number, name: string, data: any[], legend: boolean = true, step: string = 'end') {
  const lineOpt = makeStepLineOption(grid, yAxis, name, data, step)
  options.series?.push(lineOpt)
  if (legend) {
    options.legend!.data.push(name)
  }  
}

function remove(name: string, mode: number = 0) {
  let func // = (item) => item != name
  let func1
  switch (mode) {
    case 1: // wildcard
      func = item => !item.includes(name)
      func1 = item => !item.name.includes(name)
      break
    case 2: // prefix
      func = item => !item.startsWith(name)
      func1 = item => !item.name.startsWith(name)
      break
    case 3: // suffix
      func = item => !item.endsWith(name) // (item.indexOf(name, item.length - name.length) !== -1)
      func1 = item => !item.name.endsWith(name) // !(item.indexOf(name, item.length - name.length) !== -1)
      break
    case 0: // match
    default:
      func = (item) => item != name
      func1 = (item) => item.name != name 
  }

  options.legend!.data = options.legend!.data.filter(func)
  options.series = options.series!.filter(func1)
}

defineExpose({
  reset,
  addGrid,
  addAxisPointer,
  addAxis,
  addKLine,
  addLine,
  addBar,
  addStepLine,
  remove
})


</script>
<template>
  <Echart :options="options" :width="width" :height="height" />  
</template>
