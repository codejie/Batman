<!--
KLine that support add lines or data
-->
<script setup lang="ts">
import { ref } from 'vue';
import { Echart, EChartsOption } from '@/components/Echart';

const upColor = '#ec0000'
const downColor = '#00da3c'
const blankOption = {
  title: [],
  grid: [
    {
      left: '4%',
      right: '8%',
      top: '0%',
      height: '90%'
    }
  ],
  xAxis: [
    {
      type: 'category',
      gridIndex: 0,
      data: []
    }
  ],
  axisPointer: {
    label: {
      backgroundColor: '#777'
    }
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
  legend: {
    bottom: '0%',
    icon: 'circle',
    data: []
  }, 
  yAxis: [{
    type: 'value',
    gridIndex: 0,
    show: true,
    position: 'left',
    nameGap: 30,
    scale: true,
    splitArea: {
      show: true
    }
  }],
  series: []
}

let yMin: number = -1
let yMax: number = -1

const options = ref<EChartsOption>(blankOption)

function test() {
  console.log('test')
}

function reset() {
  options.value.xAxis![0].data = []
}

function setDate(data: string[]) {
  // console.log(data)
  options.value.xAxis![0].data = data
  options.value.title.push({ text: "4444" })
}

function setKLine(data: any[], markLine: boolean = true, legend: boolean = false) {
  const option = {
    name: 'KLine',
    type: 'candlestick',
    itemStyle: {
      color: upColor,
      color0: downColor
    },
    xAxisIndex: 0,
    yAxisIndex: 0,
    markLine: {
      symbol: ['none', 'none'],
      data: [] as any[]
    },
    data: data
  }
  if (markLine) {
    option.markLine.data.push({
      name: 'min',
      type: 'min',
      valueDim: 'close'
    })
    option.markLine.data.push({
      name: 'max',
      type: 'max',
      valueDim: 'close'
    })
  }

  options.value.series!.push(option)
  if (legend) {
    options.value.legend!.data.push('KLine')
  }
}

function addLine(name: string, data: number[], legend: boolean = true, fit: boolean = false, asBase: boolean = false) {
  if (asBase) {
    yMax = Math.max(...data)
    yMin = Math.min(...data)
  }

  if (fit) {
    if (yMin !== -1 && yMax !== -1) {
      
    }
  }

  const option = {
    name: name,
    type: 'line',
    xAxisIndex: 0,
    yAxisIndex: 0,
    showSymbol: false,
    lineStyle: {
      width: 1
    },
    data: data
  }
  options.value.series!.push(option)
  if (legend) {
    options.value.legend!.data.push(name)
  }
}

function removeLine(name: string) {
  options.value.series = options.value.series!.filter( item => item.name != name)
}

defineExpose({
  test,
  reset,
  setDate,
  setKLine,
  addLine,
  removeLine
})

</script>
<template>
  <Echart :options="options" />
</template>
