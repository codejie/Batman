<!--
KLine that support add lines or data
-->
<script setup lang="ts">
import { ref } from 'vue';
import { Echart, EChartsOption } from '@/components/Echart';
import { Layout_0 } from './layout/Layout_0';
import { Layout_1 } from './layout/Layout_1';

const upColor = '#ec0000'
const downColor = '#00da3c'

const layoutSet = {
  '0': Layout_0,
  '1': Layout_1
}

const currentLayout = ref<number>(0)

const blankOption = {
  title: [],
  legend: {
    bottom: '0%',
    icon: 'circle',
    data: []
  }
}

const options = ref<EChartsOption>(blankOption)

function reset() { options.value = blankOption }

function setLayout(layout: number) {
  const lo = layoutSet[layout]
  Object.assign(options.value, lo)
}

function getLayout() { return currentLayout.value }

function setXData(grid: number, data: number[] | string[]) {
  if (grid == 0) {

  }
}

function addKLine(grid: number, loc: number, name: string, data: any[], markLine: boolean = true, legend: boolean = false) {}
function addLine(grid: number, loc: number, name: string, data: number[], legend: boolean = true) {}
function addBar(grid: number, loc: number, name: string, data: number[], legend: boolean = true) {}
function remove(grid: number, loc: number, name: string) {}


defineExpose({
  reset,
  setLayout,
  getLayout,
  setXData,
  addKLine,
  addLine,
  addBar,
  remove
})


</script>
<template>
  <Echart :options="options" />
</template>
