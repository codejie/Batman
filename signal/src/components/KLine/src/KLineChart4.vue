<script setup lang="ts">
import { ref } from 'vue';
import { Echart, EChartsOption } from '@/components/Echart';

const upColor = '#ec0000'
const downColor = '#00da3c'

// const blankOption = {
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

function makeKLineOption(grid: number, name: string, data: any[]) {
  return {
    name: name,
    type: 'candlestick',
    itemStyle: {
      color: upColor,
      color0: downColor
    },
    xAxisIndex: grid,
    yAxisIndex: grid,
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

function makeLineOption(grid: number, name: string, data: any[]) {
  return {
    name: name,
    type: 'line',
    xAxisIndex: grid,
    yAxisIndex: grid,
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

function makeBarOption(grid: number, name: string, data: any[]) {
  return {
    name: name,
    type: 'bar',
    xAxisIndex: grid,
    yAxisIndex: grid,
    showSymbol: false,
    itemStyle: {
      color: (item) => {
        if (item.value.length > 2)
          return item.value[2] > 0 ? upColor : downColor
        else
          return upColor
      }
    },
    data: data
  }
}

function makeStepLineOption(grid: number, name: string, data: any[], step: string = 'end') {
  return {
    name: name,
    type: 'line',
    step: step,
    xAxisIndex: grid,
    yAxisIndex: grid,
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

const options = ref<EChartsOption>({
  title: [],
  grid: [],
  xAxis: [],
  yAxis: [],
  series: [],
  legend: {
    bottom: '0%',
    icon: 'circle',
    data: []
  }
})

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
      data: []
    }
  }
}

function addGrid(id: number, left: number | string, top: number | string, right: number | string, bottom: number | string, width?: number | string, height?: number | string) {
  options.value.grid!.push({
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
  options.value['axisPointer'] = {
    link: [
      {
        xAxisIndex: grids
      }
    ],
    label: {
      backgroundColor: '#777'
    }    
  }
  options.value['tooltip'] = {
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

function addAxis(grid: number, xdata: number[] | string[], showTick: boolean = true) {
  options.value.xAxis!.push({
    type: 'category',
    gridIndex: grid,
    data: xdata,
    boundaryGap: false,
    axisLine: { onZero: true },
    axisTick: { show: true },
    splitLine: { show: false },
    axisLabel: { show: showTick },    
  })
  options.value.yAxis!.push({
    type: 'value',
    // nameLocation : 'middle',
    show: true,
    gridIndex: grid,
    position: 'left',
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
}

function addKLine(grid: number, name: string, data: any[], markLine: boolean = true, legend: boolean = false) {
  const klineOpt = makeKLineOption(grid, name, data)
  if (markLine) {
    klineOpt.markLine.data.push(makeMarkLine(true))
    klineOpt.markLine.data.push(makeMarkLine(false))
  }
  options.value.series!.push(klineOpt)
  if (legend) {
    options.value.legend!.data.push(name)
  }
}

function addLine(grid: number, name: string, data: number[], legend: boolean = true) {
  const lineOpt = makeLineOption(grid, name, data)
  options.value.series!.push(lineOpt)
  if (legend) {
    options.value.legend!.data.push(name)
  }  
}

function addBar(grid: number, name: string, data: number[], legend: boolean = true) {
  const barOpt = makeBarOption(grid, name, data)
  options.value.series!.push(barOpt)
  if (legend) {
    options.value.legend!.data.push(name)
  }  
}

function addStepLine(grid: number, name: string, data: any[], legend: boolean = true, step: string = 'end') {
  const lineOpt = makeStepLineOption(grid, name, data, step)
  options.value.series?.push(lineOpt)
  if (legend) {
    options.value.legend!.data.push(name)
  }  
}

// function remove(name: string, wildcard: boolean = false) {
//   if (!wildcard) {
//     options.value.legend!.data = options.value.legend!.data.filter( item => item != name)
//     options.value.series = options.value.series!.filter( item => item.name != name )
//   }
//   else {
//     options.value.legend!.data = options.value.legend!.data.filter( item => ! item.includes(name) )
//     options.value.series = options.value.series!.filter( item => ! item.name.includes(name) )
//   }
// }

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

  options.value.legend!.data = options.value.legend!.data.filter(func)
  options.value.series = options.value.series!.filter(func1)
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
  <Echart :options="options" />
</template>
