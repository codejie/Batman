<!--
KLine that support add lines or data
-->
<script setup lang="ts">
import { ref } from 'vue';
import { Echart, EChartsOption } from '@/components/Echart';

const options = ref<EChartsOption>({
  title: [
    {
      text: 'KLineChart3',
      show: true
    },
    {
      text: '1111'
    }
  ],
  grid: [
    {
      left: '4%',
      right: '8%',
      top: '2%',
      height: '96%'
    }
  ],
  xAxis: [
    {
      type: 'category',
      gridIndex: 0,
      data: []
    }
  ],
  // legend: [],  
  yAxis: [{
    type: 'value',
    gridIndex: 0
  }],
  // series: [
  // ]
})

function test() {
  console.log('test')
}

function setDate(data: string[]) {
  options.value.xAxis![0].data = data
}

function setKLine(data: any[]) {

}

function addLine(data: number[]) {

}

defineExpose({
  test,
  setDateData
})

</script>
<template>
  <Echart :options="options" />
</template>
