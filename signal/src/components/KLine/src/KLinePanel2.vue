<script setup lang="ts">
import { computed, onMounted, PropType, ref, unref, watch } from 'vue';
import { ElRow, ElCol, ElButton, ElCheckboxGroup, ElCheckboxButton, ElRadioGroup, ElRadioButton, ElMessage, ElDropdown, ElDropdownMenu, ElDropdownItem, ElIcon } from 'element-plus';
import { apiCreate } from '../../../api/customized';
import { apiHistory } from '../../../api/data/stock'
import { KLineChart, KLineChart4, ReqParam, ShowParam } from '..';
import { HistoryDataModel } from '../../../api/data/stock/types';
import { apiMACD } from '@/api/libs/talib';

const props = defineProps({
  param: {
    type: Object as PropType<ReqParam>,
    required: true
  }
})
const startGroup: string[] = ['两年', '一年', '半年']
const maGroup: number[] = [5, 7, 9, 10, 12, 15, 17, 20, 26, 30, 45, 60]
const klineGroup: string[] = ['KLine', 'Zoom']
let start: string = '2023-01-01'
let zoom: boolean = false
let kline: boolean = true

const title = ref<string>('')
const startRange = ref<string>('一年')
const maLines = ref<number[]>([7, 9, 12])
const zoom_kline = ref<string[]>(['KLine'])

const kchart = ref(null)

let historyData: HistoryDataModel[] = []
let xData: string[] = []
let klineData: any[] = []
let volumeData: number[] = []

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

function initChartOptions() {
  kchart.value?.addGrid(0, '4%', '4%', '4%', '40%')
  kchart.value?.addGrid(1, '4%', '70%', '4%', '6%')
}

async function fetchHistoryData(code: string) {
  const ret = await apiHistory({
    code: code,
    start: start
  })

  historyData = ret.result
}

function setAxis(data: string[]) {
  kchart.value?.addAxis(0, data, true)
  kchart.value?.addAxis(1, data, false)
  kchart.value?.addAxisPointer([0, 1])
}

function setKLine(data: any[]) {
  kchart.value?.addKLine(0, 'KLine', data, true, true)
}

function setMALines(data: HistoryDataModel[]) {
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
  const dif = arrayData.map(item => item[0])
  const dea = arrayData.map(item => item[1])
  const macd = arrayData.map(item => item[2])
  kchart.value?.addLine(1, 'dif', dif)
  kchart.value?.addLine(1, 'dea', dea)
  kchart.value?.addLine(1, 'macd', macd)
}

function setGrid() {
  kchart.value?.reset()
  if (!zoom) {
    kchart.value?.addGrid(0, '4%', '4%', '4%', '6%')
  } else {
    kchart.value?.addGrid(0, '4%', '4%', '4%', '40%')
    kchart.value?.addGrid(1, '4%', '70%', '4%', '6%')
  }
}

function updateChartOptions(data: HistoryDataModel[]) {
  xData = data.map(item => item.date)
  klineData = data.map(({open, close, low, high}) => ([open, close, low, high]))
  volumeData = data.map(item => [item.date, item.volume, item.open > item.close ? 1 : -1])

  setAxis(xData)
  setKLine(klineData)
  setMALines(data)
  setVolumeData(volumeData)
}

onMounted(async () =>{
  const date: Date = new Date()
  date.setFullYear(date.getFullYear() - 1)
  start = date.toISOString().slice(0, 10)

  initChartOptions()
  await fetchHistoryData(props.param.code)
  updateChartOptions(historyData)
})

watch(
  () => props.param,
  async () => {
    await fetchHistoryData(props.param.code)
})


async function onCustomizedClick() {
  const ret = await apiCreate({
    code: props.param.code,
    type: 1
  })
  if (ret.code == 0) {
    ElMessage({
        type: 'success',
        message: `${props.param.code} added to customized list.`
      })    
  }
}

function onKLineChanged() {
  console.log(zoom_kline.value)
  zoom = zoom_kline.value.includes('Zoom')
  kline = zoom_kline.value.includes('KLine')
  // updateShowParam()
}

function onMaGroupChanged() {
  // maLines.value = values
  // console.log(maLines.value)
  // updateShowParam()
}

function onStartChanged() {
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
  start = date.toISOString().slice(0, 10)
  // updateDataParam(props.param.code)
}

function onGridModeChanged(param) {
  console.log(param)
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
    <ElCol :span="6">
      <ElRadioGroup v-model="startRange" size="small" style="float: right;" @change="onStartChanged">
        <ElRadioButton v-for="item in startGroup" :key="item" :value="item" :label="item" />
      </ElRadioGroup>
    </ElCol>
    <ElCol :span="10">
      <ElCheckboxGroup v-model="maLines" size="small" style="float: center; margin-right: 12px;" @change="onMaGroupChanged">
        <ElCheckboxButton v-for="item in maGroup" :key="item" :value="item" :label="item" :checked="item in maLines" />
      </ElCheckboxGroup>
    </ElCol>
    <ElCol :span="4">
      <ElDropdown size="small" @command="onGridModeChanged" @click="onGridModeChanged">
        <ElButton size="small">123<ElIcon class="el-icon--right"><arrow-down /></ElIcon></ElButton>
        <template #dropdown>
          <ElDropdownMenu>
            <ElDropdownItem>Volumn</ElDropdownItem>
            <ElDropdownItem>MACD</ElDropdownItem>
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
