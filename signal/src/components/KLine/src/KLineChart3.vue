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
  yMin = -1,
  yMax = -1
  options.value.xAxis![0].data = []
}

function setDate(data: string[]) {
  // console.log(data)
  options.value.xAxis![0].data = data
  // options.value.title.push({ text: "4444" })
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

function arrayMin(arr) {
  return arr.reduce(function (p, v) {
    if (isNaN(p)) return v
    if (isNaN(v)) return p
    return ( p < v ? p : v );
  });
}

function arrayMax(arr) {
  return arr.reduce(function (p, v) {
    if (isNaN(p)) return v
    if (isNaN(v)) return p    
    return ( p > v ? p : v );
  });
}

function getArrayRange(array: number[]) {
  return {
    max: 
      array.reduce(function (p, v) {
          if (isNaN(p)) return v
          if (isNaN(v)) return p
          return ( p > v ? p : v );
        }),
    min: 
      array.reduce(function (p, v) {
          if (isNaN(p)) return v
          if (isNaN(v)) return p
          return ( p < v ? p : v );
        })        
  }
}

function setYRange(min: number, max: number) {
  yMax = max
  yMin = min
}

function addLine(name: string, data: number[], fit: boolean = true, legend: boolean = true) {
  if (fit) {
    if (yMin !== -1 && yMax !== -1) {
      const diff1 = yMax - yMin
      const { min, max } = getArrayRange(data)
      const diff2 = max - min
      const arg1 = diff1 / diff2
      const arg2 = arg1 * min - yMin
      data = data.map(item => (arg1 * item - arg2))
      name = name + '(f)'
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
    // itemStyle: {
    //   color: '#ec0000'
    // },
    data: data.map(item => isNaN(item) ? item : item.toFixed(2))
  }
  options.value.series!.push(option)
  if (legend) {
    options.value.legend!.data.push(name)
  }
}

// function addFitLine(name: string, data: number[], legend: boolean = true) {
//   if (yMin !== -1 && yMax !== -1) {
//     const diff1 = yMax - yMin
//     const { min, max } = getArrayRange(data)
//     // const max2 = arrayMax(data)
//     // const min2 = arrayMin(data)
//     const diff2 = max - min
//     const arg1 = diff1 / diff2
//     const arg2 = arg1 * min - yMin
//     data = data.map(item => (arg1 * item - arg2))
//     name = name + '(f)'
//   } else {
//     yMax = arrayMax(data)
//     yMin = arrayMin(data)    
//   }

//   console.log(data)

//   const option = {
//     name: name,
//     type: 'line',
//     xAxisIndex: 0,
//     yAxisIndex: 0,
//     showSymbol: false,
//     lineStyle: {
//       width: 1
//     },
//     data: data.map(item => isNaN(item) ? item : item.toFixed(2))
//   }
//   options.value.series!.push(option)
//   if (legend) {
//     options.value.legend!.data.push(name)
//   }
// }

function remove(name: string, fit: boolean = false) {
  if (fit) name = name + '(f)'
  options.value.series = options.value.series!.filter(item => item.name != name)
}

function addBar(name: string, data: number[], fit: boolean = true, legend: boolean = true) {
  if (fit) {
    if (yMin !== -1 && yMax !== -1) {
      const diff1 = yMax - yMin
      const { min, max } = getArrayRange(data)
      const diff2 = max - min
      const arg1 = diff1 / diff2
      const arg2 = arg1 * min - yMin
      data = data.map(item => (arg1 * item - arg2))
      name = name + '(f)'
    }    
  }

  const option = {
    name: name,
    type: 'bar',
    xAxisIndex: 0,
    yAxisIndex: 0,
    showSymbol: false,
    itemStyle: {
      color: (item) => {
        return item.value > 0 ? upColor : downColor
      }
    },
    data: data.map(item => isNaN(item) ? item : item.toFixed(2))
  }
  options.value.series!.push(option)
  if (legend) {
    options.value.legend!.data.push(name)
  } 
}

defineExpose({
  test,
  reset,
  getArrayRange,
  setDate,
  setKLine,
  addLine,
  addBar,
  // addFitLine,
  remove,

})

</script>
<template>
  <Echart :options="options" />
</template>
