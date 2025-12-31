<script setup lang="ts">
import { onMounted, PropType, ref, watch } from 'vue'
import {
  ElRow,
  ElCol,
  ElButton,
  ElCheckboxGroup,
  ElCheckboxButton,
  ElRadioGroup,
  ElRadioButton,
  ElMessage,
  ElDropdown,
  ElDropdownMenu,
  ElDropdownItem
} from 'element-plus'
import { KLineChartPro, ReqParam } from '..'
import { apiMACD } from '@/api/libs/talib'
import { apiGetMinuteData, MinuteDataItem } from '@/api/data'
import { apiCreate } from '@/api/customized'

/**
 * Minute-level K-Line Panel (Optimized)
 * Supports time ranges: 1D, 3D, 5D
 * Supports MA periods: 5, 10, 15, 60
 * Uses English keys from Baostock minute data
 */

type InitParam = {
  maGroup: number[]
  maLines: number[]
  zoom: boolean
  volume: boolean
  period: string
}

const props = defineProps({
  reqParam: {
    type: Object as PropType<ReqParam>,
    required: true
  },
  initParam: {
    type: Object as PropType<InitParam>,
    required: false,
    default: () => {
      return {
        maGroup: [5, 10, 15, 60],
        maLines: [5, 10, 15],
        zoom: false,
        volume: true,
        period: '5' // Default to 5-minute data as it's more common
      }
    }
  }
})

const rangeGroup: string[] = ['1天', '3天', '5天']
const maGroup: number[] = props.initParam.maGroup
const klineGroup: string[] = ['KLine', 'Zoom']

const currentRange = ref<string>('1天')
const maLines = ref<number[]>(props.initParam.maLines)
const zoom_kline = ref<string[]>(['KLine'])
const grid2Mode = ref<string>(props.initParam.volume ? 'Volume' : 'MACD')

const kchart = ref<InstanceType<typeof KLineChartPro>>()

let minuteData: MinuteDataItem[] = []
let xData: string[] = []
let klineData: any[] = []
let volumeData: any[] = []

/**
 * Simple MA calculation
 */
function calcMAData(ma: number, data: number[]) {
  const result: any[] = []
  for (let i = 0, len = data.length; i < len; i++) {
    if (i < ma - 1) {
      result.push('-')
      continue
    }
    let sum = 0
    for (let j = 0; j < ma; j++) {
      sum += +data[i - j]
    }
    result.push((sum / ma).toFixed(2))
  }
  return result
}

/**
 * Fetch minute data from API
 */
async function fetchMinuteData() {
  console.log(props.reqParam)
  const period = props.reqParam.period || props.initParam.period
  const start = props.reqParam.start || getStartDate(currentRange.value)
  const end = props.reqParam.end || getEndDate()
  console.log(period, start, end)
  const ret = await apiGetMinuteData({
    type: props.reqParam.type,
    codes: [props.reqParam.code],
    start: start,
    end: end,
    period: period,
    adjust: props.reqParam.adjust || 'qfq'
  })

  if (ret.result && ret.result.length > 0) {
    minuteData = ret.result[0] || []
  } else {
    minuteData = []
  }
}

/**
 * Update chart configuration based on current state
 */
async function resetChart() {
  const isZoom = zoom_kline.value.includes('Zoom')
  const showKLine = zoom_kline.value.includes('KLine')
  
  if (!kchart.value) return
  
  kchart.value.reset()
  
  // Configure Grids matching KLinePanel2
  if (isZoom) {
    kchart.value.addGridNew({ id: 0, left: '4%', top: '4%', right: '4%', bottom: '10%' })
  } else {
    kchart.value.addGridNew({ id: 0, left: '4%', top: '4%', right: '4%', bottom: '40%' })
    kchart.value.addGridNew({ id: 1, left: '4%', top: '70%', right: '4%', bottom: '6%' })
  }

  // Set Axes
  kchart.value.addAxis(0, xData, true, true) // Enable scale for Price axis
  if (!isZoom) {
    kchart.value.addAxis(1, xData, false, false) // Disable scale for MACD/Volume to center zero
    kchart.value.addAxisPointer([0, 1])
  } else {
    kchart.value.addAxisPointer([0])
  }

  // Set Candlestick
  if (showKLine) {
    kchart.value.addKLine(0, 'KLine', klineData, { markLine: true, legend: true })
  }

  // Set MA Lines
  if (maLines.value.length > 0) {
    const closeData = minuteData.map((item) => item.close)
    for (const ma of maLines.value) {
      kchart.value.addLine(0, `MA${ma}`, calcMAData(ma, closeData))
    }
  }

  // Lower Grid Contents
  if (!isZoom) {
    if (grid2Mode.value === 'Volume') {
      kchart.value.addBar(1, 'Volume', volumeData, { legend: true })
    } else if (grid2Mode.value === 'MACD') {
      await setMACD()
    }
  }

  // Always enable DataZoom for minute data as it can be dense
  kchart.value.addDataZoom()
}

/**
 * Calculate and set MACD series
 */
async function setMACD() {
  if (!kchart.value) return
  const closeData = minuteData.map((item) => item.close)
  const ret = await apiMACD({ value: closeData })
  const arrayData = ret.result.data
  
  const dif: any[] = []
  const dea: any[] = []
  const macd: any[] = []
  
  for (let i = 0; i < minuteData.length; ++i) {
    const dateLabel = xData[i]
    dif.push([dateLabel, Number(parseFloat(arrayData[i][0]).toFixed(3))])
    dea.push([dateLabel, Number(parseFloat(arrayData[i][1]).toFixed(3))])
    macd.push([
      dateLabel,
      Number(parseFloat(arrayData[i][2]).toFixed(3)),
      arrayData[i][2] >= 0 ? 1 : -1
    ])
  }
  
  kchart.value.addLine(1, 'DIF', dif, { legend: true })
  kchart.value.addLine(1, 'DEA', dea, { legend: true })
  kchart.value.addBar(1, 'MACD', macd, { legend: true })
}

/**
 * Map raw minute data to chart-compatible format
 */
function updateChartData(data: MinuteDataItem[]) {
  // Combine date and time for X-axis labels (e.g., 2023-10-27 09:30:00)
  xData = data.map((item) => `${item.time}`)
  klineData = data.map(({ open, close, low, high }) => [open, close, low, high])
  volumeData = data.map((item, idx) => [xData[idx], item.volume, item.open <= item.close ? 1 : -1])
  resetChart()
}

/**
 * Handle time range changes (1D, 3D, 5D)
 */
async function onRangeChanged() {
  await fetchMinuteData()
  updateChartData(minuteData)
}

/**
 * Utility to calculate end date (tomorrow)
 */
function getEndDate() {
  const date = new Date()
  date.setDate(date.getDate() + 1) // Tomorrow
  return date.toISOString().slice(0, 10)
}

/**
 * Utility to calculate start date string based on range
 * 1天: today to tomorrow
 * 3天: 2 days ago (前天) to tomorrow
 * 5天: 4 days ago (大前天) to tomorrow
 */
function getStartDate(range: string) {
  const date = new Date()
  switch (range) {
    case '1天':
      // Today (0 days back)
      break
    case '3天':
      // 前天 (2 days ago)
      date.setDate(date.getDate() - 2)
      break
    case '5天':
      // 大前天 (4 days ago)
      date.setDate(date.getDate() - 4)
      break
  }
  return date.toISOString().slice(0, 10)
}

function onMaLinesChanged() {
  resetChart()
}

function onKLineOptionsChanged() {
  resetChart()
}

function onGridModeChanged(command: string) {
  grid2Mode.value = command
  resetChart()
}

async function onCustomizedClick() {
  const ret = await apiCreate({
    code: props.reqParam.code,
    type: props.reqParam.type
  })
  if (ret.code == 0) {
    ElMessage.success(`${props.reqParam.code} 已加入自选列表`)
  }
}

onMounted(async () => {
  await fetchMinuteData()
  updateChartData(minuteData)
})

watch(
  () => props.reqParam.code,
  async () => {
    await fetchMinuteData()
    updateChartData(minuteData)
  }
)

defineExpose({
  minuteData
})
</script>

<template>
  <div class="kline-panel-pro">
    <ElRow :gutter="12" class="mb-3" align="middle">
      <ElCol :span="3">
        <ElButton size="small" type="primary" plain @click="onCustomizedClick">加入自选</ElButton>
      </ElCol>
      
      <ElCol :span="5">
        <ElRadioGroup v-model="currentRange" size="small" @change="onRangeChanged">
          <ElRadioButton v-for="item in rangeGroup" :key="item" :label="item" :value="item" />
        </ElRadioGroup>
      </ElCol>
      
      <ElCol :span="8">
        <ElCheckboxGroup v-model="maLines" size="small" @change="onMaLinesChanged">
          <ElCheckboxButton v-for="ma in maGroup" :key="ma" :label="ma" :value="ma">
            MA{{ ma }}
          </ElCheckboxButton>
        </ElCheckboxGroup>
      </ElCol>
      
      <ElCol :span="8" class="text-right">
        <ElDropdown size="small" trigger="click" @command="onGridModeChanged">
          <ElButton size="small" :disabled="zoom_kline.includes('Zoom')">
            {{ grid2Mode }} <i class="el-icon-arrow-down el-icon--right"></i>
          </ElButton>
          <template #dropdown>
            <ElDropdownMenu>
              <ElDropdownItem command="Volume">Volume</ElDropdownItem>
              <ElDropdownItem command="MACD">MACD</ElDropdownItem>
            </ElDropdownMenu>
          </template>
        </ElDropdown>
        
        <ElCheckboxGroup v-model="zoom_kline" size="small" class="d-inline-block ml-2" @change="onKLineOptionsChanged">
          <ElCheckboxButton v-for="item in klineGroup" :key="item" :label="item" :value="item">
            {{ item }}
          </ElCheckboxButton>
        </ElCheckboxGroup>
      </ElCol>
    </ElRow>
    
    <div class="chart-container">
      <KLineChartPro ref="kchart" height="500px" />
    </div>
  </div>
</template>

<style scoped>
.kline-panel-pro {
  padding: 10px;
}
.mb-3 {
  margin-bottom: 12px;
}
.text-right {
  text-align: right;
}
.d-inline-block {
  display: inline-block;
}
.ml-2 {
  margin-left: 8px;
}
.chart-container {
  background-color: #fff;
  border-radius: 4px;
}
</style>
