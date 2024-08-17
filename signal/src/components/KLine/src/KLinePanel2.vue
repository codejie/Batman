<script setup lang="ts">
import { onMounted, PropType, ref, watch } from 'vue';
import { ElRow, ElCol, ElButton, ElCheckboxGroup, ElCheckboxButton, ElRadioGroup, ElRadioButton, ElMessage, ElDropdown, ElDropdownMenu, ElDropdownItem } from 'element-plus';
import { apiCreate } from '../../../api/customized';
import { apiHistory } from '../../../api/data/stock'
import { KLineChart4, ReqParam } from '..';
import { HistoryDataModel } from '../../../api/data/stock/types';
import { apiMACD } from '@/api/libs/talib';

type InitParam = {
  // startGroup: string[],
  // startRange: string,
  maGroup: number[],
  maLines: number[],
  zoom: boolean,
  volume: boolean
}

const props = defineProps({
  reqParam: {
    type: Object as PropType<ReqParam>,
    required: false
  },
  initParam: {
    type: Object as PropType<InitParam>,
    required: false,
    default: () => {
      return {
        maGroup: [5, 7, 9, 10, 12, 15, 17, 20, 26, 30, 45, 60],
        maLines: [7, 9, 12],
        zoom: false,
        volume: true
      }
    }
  }
})

const startGroup: string[] = ['两年', '一年', '半年']
const maGroup: number[] = props.initParam.maGroup // [5, 7, 9, 10, 12, 15, 17, 20, 26, 30, 45, 60]
const klineGroup: string[] = ['KLine', 'Zoom']
let zoom: boolean = props.initParam.zoom // false
let kline: boolean = true

const startRange = ref<string>()
const maLines = ref<number[]>(props.initParam.maLines) // [7, 9, 12])
const zoom_kline = ref<string[]>(['KLine'])
const grid2Mode = ref<string>(props.initParam.volume ? 'Volume' : 'MACD')

const kchart = ref(null)

let historyData: HistoryDataModel[] = []
let xData: string[] = []
let klineData: any[] = []
let volumeData: any[] = []

defineExpose({
  historyData: historyData
})

function calcMAData(ma: number, data: number[]) {
  var result: any[] = [];
  for (var i = 0, len = data.length; i < len; i++) {
    if (i < ma) {
      result.push('-')
      continue;
    }
    var sum = 0;
    for (var j = 0; j < ma; j++) {
      sum += +data[i - j]
    }
    result.push((sum / ma).toFixed(2))
  }
  return result
}

async function fetchHistoryData() {
  const ret = await apiHistory({
    code: props.reqParam!.code,
    start: props.reqParam!.start,
    end: props.reqParam!.end
  })

  historyData = ret.result
}

function setAxis(data: string[]) {
  if (zoom) {
    kchart.value?.addAxis(0, data, true)
    kchart.value?.addAxisPointer([0])
  } else {
    kchart.value?.addAxis(0, data, true)
    kchart.value?.addAxis(1, data, false)
    kchart.value?.addAxisPointer([0, 1])
  }
}

function setKLine(data: any[]) {
  if (kline) {
    kchart.value?.addKLine(0, 'KLine', data, true, true)
  } else {
    kchart.value?.remove('KLine')
  }
}

function setMALines(data: HistoryDataModel[]) {
  kchart.value?.remove('MA', true)

  if (maLines.value.length > 0) {
    const closeData = data.map(item => item.close)
    for (const ma of maLines.value) {
      kchart.value?.addLine(0, `MA${ma}`, calcMAData(ma, closeData))
    }
  }  
}

function setVolumeData(data: any[]) {
  kchart.value?.addBar(1, 'Volume', data, true)  
}

async function setMACD(data: HistoryDataModel[]) {
  const closeData = data.map(item => item.close)
  const ret = await apiMACD({
    value: closeData    
  })
  const arrayData = ret.result.data
  const dif: any[] = []
  const dea: any[] = []
  const macd: any[] = []
  for (let i = 0; i < data.length; ++ i) {
    dif.push([data[i]['date'], parseFloat(arrayData[i][0]).toFixed(2)])
    dea.push([data[i]['date'], parseFloat(arrayData[i][1]).toFixed(2)])
    macd.push([data[i]['date'], parseFloat(arrayData[i][2]).toFixed(2), arrayData[i][2] >= 0 ? 1 : -1]);
  }
  kchart.value?.addLine(1, 'DIF', dif)
  kchart.value?.addLine(1, 'DEA', dea)
  kchart.value?.addBar(1, 'MACD', macd)
}

function resetGrid2(mode: string) {
  if (mode == 'Volume') {
    kchart.value?.remove('DIF')
    kchart.value?.remove('DEA')
    kchart.value?.remove('MACD')

    setVolumeData(volumeData)
  } else {
    kchart.value?.remove('Volume')
    setMACD(historyData)
  }
}

function setGrid() {
  kchart.value?.reset()
  if (zoom) {
    kchart.value?.addGrid(0, '4%', '4%', '4%', '10%')
  } else {
    kchart.value?.addGrid(0, '4%', '4%', '4%', '40%')
    kchart.value?.addGrid(1, '4%', '70%', '4%', '6%')
  }
}

function resetChart() {
  setGrid()
  setAxis(xData)
  setKLine(klineData)
  setMALines(historyData)
  if (!zoom) {
    resetGrid2(grid2Mode.value)
  }
}

function updateChartOptions(data: HistoryDataModel[]) {
  xData = data.map(item => item.date)
  klineData = data.map(({open, close, low, high}) => ([open, close, low, high]))
  volumeData = data.map(item => [item.date, item.volume, item.open > item.close ? 1 : -1])

  resetChart()
}

onMounted(async () =>{
  if (props.reqParam) {
    if (!props.reqParam!.start) {
      const date: Date = new Date()
      date.setFullYear(date.getFullYear() - 1)
      props.reqParam!.start = date.toISOString().slice(0, 10)
    }

    // initChartOptions()
    await fetchHistoryData()
    updateChartOptions(historyData)
  }
})

watch(
  () => props.reqParam,
  async () => {
    await fetchHistoryData()
    updateChartOptions(historyData)
})


async function onCustomizedClick() {
  const ret = await apiCreate({
    code: props.reqParam.code,
    type: 1
  })
  if (ret.code == 0) {
    ElMessage({
        type: 'success',
        message: `${props.reqParam.code} added to customized list.`
      })    
  }
}

function onKLineChanged() {
  zoom = zoom_kline.value.includes('Zoom')
  kline = zoom_kline.value.includes('KLine')
  resetChart()
  setKLine(klineData)
}

function onMaGroupChanged() {
  setMALines(historyData)
}

async function onStartChanged() {
  const date: Date = new Date()
  switch(startRange.value) {
    case '两年':
      date.setFullYear(date.getFullYear() - 2)
      break
    case '半年':
      date.setMonth(date.getMonth() - 6)
      break
    case '一年':
    default:
      date.setFullYear(date.getFullYear() - 1)
  }
  props.reqParam!.start = date.toISOString().slice(0, 10)

  await fetchHistoryData()
  updateChartOptions(historyData)
}

function onGridModeChanged(mode) {
  grid2Mode.value = mode
  resetGrid2(grid2Mode.value)
}

</script>
<template>
  <ElRow :gutter="24">
    <ElCol :span="4">
      <div style="float: left;">
        <!-- {{ title }} -->
        <ElButton size="small" @click="onCustomizedClick">Add to Customized</ElButton>
      </div>
    </ElCol>
    <ElCol :span="5">
      <ElRadioGroup v-model="startRange" size="small" style="float: right;" @change="onStartChanged">
        <ElRadioButton v-for="item in startGroup" :key="item" :value="item" :label="item" />
      </ElRadioGroup>
    </ElCol>
    <ElCol :span="9">
      <ElCheckboxGroup v-model="maLines" size="small" style="float: center; margin-right: 12px;" @change="onMaGroupChanged">
        <ElCheckboxButton v-for="item in maGroup" :key="item" :value="item" :label="item" :checked="item in maLines" />
      </ElCheckboxGroup>
    </ElCol>
    <ElCol :span="6">
      <ElDropdown :disabled="zoom_kline.includes('Zoom')" ize="small" trigger="click" @command="onGridModeChanged">
        <ElButton :disabled="zoom_kline.includes('Zoom')" size="small">{{ grid2Mode }}</ElButton>
        <template #dropdown>
          <ElDropdownMenu>
            <ElDropdownItem command="Volume">Volume</ElDropdownItem>
            <ElDropdownItem command="MACD">MACD</ElDropdownItem>
          </ElDropdownMenu>
        </template>
      </ElDropdown>
      <ElCheckboxGroup v-model="zoom_kline" size="small" style="float: right;" @change="onKLineChanged">
        <ElCheckboxButton v-for="item in klineGroup" :key="item" :value="item" :label="item" :checked="item in zoom_kline" />
      </ElCheckboxGroup>        
    </ElCol>
  </ElRow>
  <ElRow :gutter="24" style="margin-top: 12px;">
    <KLineChart4 ref="kchart" />
  </ElRow> 
</template>
<style lang="css">
</style>
