<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { apiGetHistoryData } from '@/api/data'
import {
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElSelect,
  ElOption,
  ElButton,
  ElTable,
  ElTableColumn,
  ElRow,
  ElCol,
  ElDivider
} from 'element-plus'
import { AlgorithmCategoryDefinitions, AlgorithmTypeDefinitions } from '@/api/calc/defines'
import { Echart, EChartsOption } from '@/components/Echart'
import type { SeriesDataItem } from '@/components/Chart/types'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  stock: {
    type: Object,
    required: true
  },
  result: {
    type: Object,
    required: true
  },
  dataPeriodStart: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:visible'])

const xAxisData = ref<string[]>([])
const chartSeries = ref<{ name: string; series: SeriesDataItem[] }[]>([])

const title = computed(() => {
  if (!props.stock || !props.result) return ''
  const category = AlgorithmCategoryDefinitions[props.result.category]?.title || props.result.category
  const type =
    AlgorithmTypeDefinitions[props.result.category]?.types?.[props.result.type]?.title ||
    props.result.type
  const args = props.result.arguments
    ? ` (${Object.entries(props.result.arguments)
        .map(([k, v]) => `${k}=${v}`)
        .join(', ')})`
    : ''
  return `${props.stock.name}(${props.stock.code}) - ${category}: ${type}${args} - 模拟回测`
})

const chartOptions = computed<EChartsOption>(() => ({
  tooltip: {
    trigger: 'axis',
    formatter: (params) => {
      if (!Array.isArray(params) || params.length === 0) {
        return
      }

      const topSeriesCount = chartSeries.value.find(s => s.name === 'Price')?.series.length || 0
      const middleSeriesCount = chartSeries.value.find(s => s.name === 'Volume')?.series.length || 0

      const topParams = params.filter((p) => p.seriesIndex < topSeriesCount)
      const middleParams = params.filter(
        (p) =>
          p.seriesIndex >= topSeriesCount && p.seriesIndex < topSeriesCount + middleSeriesCount
      )
      const bottomParams = params.filter(
        (p) => p.seriesIndex >= topSeriesCount + middleSeriesCount
      )

      let tooltipContent = `${params[0].axisValueLabel}<br/>`

      const formatParam = (param) => {
        const seriesName = param.seriesName
        const value = param.value
        const marker = param.marker
        let formattedValue = ''

        if (value === null || value === undefined || value === '-') {
          formattedValue = '-'
        } else if (param.seriesName === 'K-Line') {
          const data = value as number[]
          formattedValue = `O:${data[1].toFixed(2)} C:${data[2].toFixed(2)} L:${data[3].toFixed(2)} H:${data[4].toFixed(2)}`
        } else if (typeof value === 'number') {
          formattedValue = value.toFixed(2)
        } else if (value && typeof (value as { value: number }).value === 'number') {
          formattedValue = (value as { value: number }).value.toString()
        } else {
          formattedValue = value.toString()
        }
        return `${marker} ${seriesName}: <b>${formattedValue}</b><br/>`
      }

      if (topParams.length > 0) {
        topParams.forEach((param) => {
          tooltipContent += formatParam(param)
        })
      }

      if (middleParams.length > 0) {
        tooltipContent += '<hr style="margin: 5px 0; border-style: dashed;"/>'
        middleParams.forEach((param) => {
          tooltipContent += formatParam(param)
        })
      }

      if (bottomParams.length > 0) {
        tooltipContent += '<hr style="margin: 5px 0; border-style: dashed;"/>'
        bottomParams.forEach((param) => {
          tooltipContent += formatParam(param)
        })
      }

      return tooltipContent
    }
  },
  axisPointer: {
      link: [{ xAxisIndex: 'all' }],
      label: {
        backgroundColor: '#777'
      }
  },
  grid: [
    { left: '5%', right: '5%', height: '40%', top: '10%' },
    { left: '5%', right: '5%', top: '55%', height: '20%' },
    { left: '5%', right: '5%', top: '80%', height: '20%' }
  ],
  xAxis: [
    { type: 'category', data: xAxisData.value, scale: true, boundaryGap: false, axisLine: { onZero: false }, splitLine: { show: false }, splitNumber: 20, min: 'dataMin', max: 'dataMax' },
    { type: 'category', gridIndex: 1, data: xAxisData.value, scale: true, boundaryGap: false, axisLine: { onZero: false }, axisTick: { show: false }, splitLine: { show: false }, axisLabel: { show: false }, splitNumber: 20, min: 'dataMin', max: 'dataMax' },
    { type: 'category', gridIndex: 2, data: xAxisData.value, scale: true, boundaryGap: false, axisLine: { onZero: false }, axisTick: { show: false }, splitLine: { show: false }, axisLabel: { show: false }, splitNumber: 20, min: 'dataMin', max: 'dataMax' }
  ],
  yAxis: [
    { scale: true, splitArea: { show: true } },
    { scale: true, gridIndex: 1, splitNumber: 2, axisLabel: { show: false }, axisLine: { show: false }, axisTick: { show: false }, splitLine: { show: false } },
    { scale: true, gridIndex: 2, splitNumber: 2, axisLabel: { show: false }, axisLine: { show: false }, axisTick: { show: false }, splitLine: { show: false } }
  ],
  series: [
    ...(chartSeries.value.find(s => s.name === 'Price')?.series || []),
    ...(chartSeries.value.find(s => s.name === 'Volume')?.series.map(s => ({ ...s, xAxisIndex: 1, yAxisIndex: 1 })) || []),
    ...(chartSeries.value.find(s => s.name === 'Calc')?.series.map(s => ({ ...s, xAxisIndex: 2, yAxisIndex: 2 })) || [])
  ]
}))

const capitalOptions = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
const priceStrategyOptions = ['开盘价', '收盘价', '最高价', '最低价', '中间价']
const buyQuantityStrategyOptions = ['全仓(资金)', '1/2(资金)', '1/3(资金)', '1/4(资金)', '全仓(持仓)', '1/2(持仓)', '1/3(持仓)', '1/4(持仓)']
const sellQuantityStrategyOptions = ['全仓(持仓)', '1/2(持仓)', '1/3(持仓)', '1/4(持仓)']
const timingStrategyOptions = ['无条件', '+1%(现价)', '+3%(现价)', '+5%(现价)', '+10%(现价)', '+15%(现价)', '-15%(现价)', '-10%(现价)', '-5%(现价)', '-3%(现价)', '-1%(现价)', '+1%(成本)', '+3%(成本)', '+5%(成本)', '+10%(成本)', '+15%(成本)', '-15%(成本)', '-10%(成本)', '-5%(成本)', '-3%(成本)', '-1%(成本)']

const form = ref({
  capital: 6, // Corresponds to 100000
  buyPriceStrategy: 0,
  buyQuantityStrategy: 1,
  buyTimingStrategy: 0,
  sellPriceStrategy: 0,
  sellQuantityStrategy: 1,
  sellTimingStrategy: 0
})

const tableData = ref([])
const totalAmount = computed(() => {
  const selectedCapital = capitalOptions[form.value.capital]
  return selectedCapital + tableData.value.reduce((sum, item) => sum + item.fee, 0)
})

const onExecute = () => {
  // todo
}

const handleClose = () => {
  emit('update:visible', false)
  xAxisData.value = []
  chartSeries.value = []
}

const getCalcChartData = (
  calcData: any,
  reportData: any[]
): { seriesData: SeriesDataItem[]; xAxisData: string[] } => {
  if (!calcData || !calcData['日期']) {
    return { seriesData: [], xAxisData: [] }
  }

  const reportTrendMap = new Map(reportData.map((r) => [r.index, r.trend]))
  const xAxisData = calcData['日期']
  const seriesData: SeriesDataItem[] = []
  let isFirstSeries = true

  for (const key in calcData) {
    if (key !== '日期' && key !== 'Signal') {
      const seriesValues = calcData[key]
      let markPointData = {}

      if (isFirstSeries) {
        const reportPoints = seriesValues
          .map((value, i) => {
            const date = xAxisData[i]
            if (reportTrendMap.has(date) && typeof value === 'number') {
              const trend = reportTrendMap.get(date)
              return {
                xAxis: date,
                yAxis: value,
                symbol: 'triangle',
                symbolRotate: trend === 1 ? 0 : 180,
                symbolSize: 8,
                itemStyle: {
                  color: trend === 1 ? '#ec0000' : '#00da3c'
                }
              }
            }
            return null
          })
          .filter((p) => p !== null)

        if (reportPoints.length > 0) {
          markPointData = { data: reportPoints }
        }
        isFirstSeries = false
      }

      seriesData.push({
        name: key,
        type: 'line',
        data: seriesValues,
        showSymbol: false,
        lineStyle: { width: 1 },
        markPoint: markPointData
      })
    }
  }
  return { seriesData, xAxisData }
}

const calculateMA = (dayCount: number, data: any[]) => {
  var result = [];
  for (var i = 0, len = data.length; i < len; i++) {
    if (i < dayCount) {
      result.push('-');
      continue;
    }
    var sum = 0;
    for (var j = 0; j < dayCount; j++) {
      sum += data[i - j].收盘;
    }
    result.push(parseFloat((sum / dayCount).toFixed(2)));
  }
  return result;
}

watch(
  () => props.visible,
  (val) => {
    if (val) {
      apiGetHistoryData({ code: props.stock.code, type: props.stock.type, start: props.dataPeriodStart }).then((res) => {
        if (res.result) {
          const history = res.result
          xAxisData.value = history.map((item: any) => item.日期)
          const klineData = history.map((item: any) => [item.开盘, item.收盘, item.最低, item.最高])
          const volumeData = history.map((item: any) => ({
            value: item.成交量,
            itemStyle: {
              color: item.开盘 > item.收盘 ? '#14b143' : '#ef232a'
            }
          }))

          const klineSeries = [
            { name: 'K-Line', type: 'candlestick', data: klineData },
            { name: 'MA5', type: 'line', data: calculateMA(5, history), symbol: 'none', lineStyle: { width: 1 } },
            { name: 'MA10', type: 'line', data: calculateMA(10, history), symbol: 'none', lineStyle: { width: 1 } },
            { name: 'MA15', type: 'line', data: calculateMA(15, history), symbol: 'none', lineStyle: { width: 1 } }
          ]

          const volumeSeries = [{ name: 'Volume', type: 'bar', data: volumeData }]

          const calcSeries = {
            name: 'Calc',
            series: getCalcChartData(props.result.calc, props.result.report).seriesData
          }

          chartSeries.value = [
            { name: 'Price', series: klineSeries },
            { name: 'Volume', series: volumeSeries },
            calcSeries
          ]
        }
      })
    }
  },
  { immediate: true }
)

</script>

<template>
  <el-dialog
    :title="title"
    :model-value="visible"
    width="60%"
    @close="handleClose"
  >
    <el-row>
      <el-col :span="24">
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
          <Echart v-if="xAxisData.length" :options="chartOptions" :height="'400px'" />
          <div v-else style="width: 100%; height: 400px; display: flex; justify-content: center; align-items: center;">Loading chart...</div>
        </div>
      </el-col>
    </el-row>
    <el-divider />
    <el-row :gutter="20">
      <el-col :span="8">
        <el-form :model="form" label-width="120px">
          <el-form-item label="本金">
            <el-select v-model="form.capital" placeholder="please select" style="width: 100%">
              <el-option
                v-for="(item, index) in capitalOptions"
                :key="index"
                :label="item"
                :value="index"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="买入价格策略">
            <el-select v-model="form.buyPriceStrategy" placeholder="please select" style="width: 100%">
              <el-option
                v-for="(item, index) in priceStrategyOptions"
                :key="index"
                :label="item"
                :value="index"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="买入数量策略">
            <el-select v-model="form.buyQuantityStrategy" placeholder="please select" style="width: 100%">
              <el-option
                v-for="(item, index) in buyQuantityStrategyOptions"
                :key="index"
                :label="item"
                :value="index"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="买入时机策略">
            <el-select v-model="form.buyTimingStrategy" placeholder="please select" style="width: 100%">
              <el-option
                v-for="(item, index) in timingStrategyOptions"
                :key="index"
                :label="item"
                :value="index"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="卖出价格策略">
            <el-select v-model="form.sellPriceStrategy" placeholder="please select" style="width: 100%">
              <el-option
                v-for="(item, index) in priceStrategyOptions"
                :key="index"
                :label="item"
                :value="index"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="卖出数量策略">
            <el-select v-model="form.sellQuantityStrategy" placeholder="please select" style="width: 100%">
              <el-option
                v-for="(item, index) in sellQuantityStrategyOptions"
                :key="index"
                :label="item"
                :value="index"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="卖出时机策略">
            <el-select v-model="form.sellTimingStrategy" placeholder="please select" style="width: 100%">
              <el-option
                v-for="(item, index) in timingStrategyOptions"
                :key="index"
                :label="item"
                :value="index"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <div style="width: 100%; text-align: right;">
              <el-button type="primary" @click="onExecute">执行</el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="16">
        <div style="display: flex; flex-direction: column; align-items: center;">
          <el-table :data="tableData" style="width: 90%">
            <el-table-column prop="index" label="序号" />
            <el-table-column prop="date" label="日期" />
            <el-table-column prop="action" label="操作" />
            <el-table-column prop="price" label="价格" />
            <el-table-column prop="quantity" label="数量" />
            <el-table-column prop="fee" label="手续费" />
          </el-table>
          <div style="width: 90%; margin-top: 10px; text-align: right;">
            统计: {{ totalAmount }}
          </div>
        </div>
      </el-col>
    </el-row>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">确认</el-button>
      </span>
    </template>
  </el-dialog>
</template>