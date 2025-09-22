<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { apiGetHistoryData } from '@/api/data'
import {
  ElDialog,
  ElForm,
  ElFormItem,
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

import { generateCalcChartSeries,calcMAData } from '@/calc/analyis/chart'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  stock: {
    type: Object,
    default: null
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

const historyData = ref<any[]>([])
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
  return `${props.stock.name}(${props.stock.code}) - ${category}: ${type}${args}`
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
    { left: '5%', right: '5%', height: '40%', top: '4%' },
    { left: '5%', right: '5%', top: '54%', height: '20%' },
    { left: '5%', right: '5%', height: '20%', bottom: '2%' }
  ],
  xAxis: [
    { type: 'category', data: xAxisData.value, scale: true, boundaryGap: false, axisLine: { onZero: false }, splitLine: { show: false }, splitNumber: 20, min: 'dataMin', max: 'dataMax' },
    { type: 'category', gridIndex: 1, data: xAxisData.value, scale: true, boundaryGap: false, axisLine: { onZero: false }, axisTick: { show: false }, splitLine: { show: false }, axisLabel: { show: false }, splitNumber: 20, min: 'dataMin', max: 'dataMax' },
    { type: 'category', gridIndex: 2, data: xAxisData.value, scale: true, boundaryGap: false, axisLine: { onZero: true, show: true }, axisTick: { show: false }, splitLine: { show: false }, axisLabel: { show: false }, splitNumber: 20, min: 'dataMin', max: 'dataMax' }
  ],
  yAxis: [
    { scale: true, splitArea: { show: true } },
    { scale: true, gridIndex: 1, splitNumber: 2, axisLabel: { show: true }, axisLine: { show: true }, axisTick: { show: true }, splitLine: { show: false } },
    { scale: true, gridIndex: 2, splitNumber: 2, axisLabel: { show: true }, axisLine: { show: true }, axisTick: { show: true }, splitLine: { show: false } }
  ],
  series: [
    ...(chartSeries.value.find(s => s.name === 'Price')?.series || []),
    ...(chartSeries.value.find(s => s.name === 'Volume')?.series.map(s => ({ ...s, xAxisIndex: 1, yAxisIndex: 1 })) || []),
    ...(chartSeries.value.find(s => s.name === 'Calc')?.series.map(s => ({ ...s, xAxisIndex: 2, yAxisIndex: 2 })) || [])
  ]
}))

const capitalOptions = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
const priceStrategyOptions = ['开盘价', '收盘价', '最高价', '最低价', '中间价']
const buyQuantityStrategyOptions = ['全仓(资金)', '1/2(资金)', '1/3(资金)', '1/4(资金)']
const sellQuantityStrategyOptions = ['全仓(持仓)', '1/2(持仓)', '1/3(持仓)', '1/4(持仓)']
const timingStrategyOptions = ['无条件', '+1%(现价)', '+3%(现价)', '+5%(现价)', '+10%(现价)', '+15%(现价)', '-15%(现价)', '-10%(现价)', '-5%(现价)', '-3%(现价)', '-1%(现价)', '+1%(成本)', '+3%(成本)', '+5%(成本)', '+10%(成本)', '+15%(成本)', '-15%(成本)', '-10%(成本)', '-5%(成本)', '-3%(成本)', '-1%(成本)']

const BUY_COMMISSION_RATE = 0
const SELL_COMMISSION_RATE = 0

const formRef = ref<InstanceType<typeof ElForm> | null>(null)
const tableMaxHeight = ref(400)
const tableData = ref<any[]>([])

const form = ref({
  capital: 6, // Corresponds to 100000
  buyPriceStrategy: 0,
  buyQuantityStrategy: 0,
  buyTimingStrategy: 0,
  sellPriceStrategy: 0,
  sellQuantityStrategy: 0,
  sellTimingStrategy: 0
})

const totalAmount = computed(() => {
  if (tableData.value.length === 0) {
    return '0.00'
  }
  const initialCapital = capitalOptions[form.value.capital]
  const lastTransaction = tableData.value[tableData.value.length - 1]
  const finalCapital = parseFloat(lastTransaction.capital)
  const profit = finalCapital - initialCapital
  return profit.toFixed(2)
})

const totalProfitRate = computed(() => {
  if (tableData.value.length === 0) {
    return '0.00%'
  }
  const initialCapital = capitalOptions[form.value.capital]
  if (initialCapital === 0) {
    return '0.00%'
  }
  const profit = parseFloat(totalAmount.value)
  const rate = (profit / initialCapital) * 100
  return `${rate.toFixed(2)}%`
})

const onExecute = () => {
  tableData.value = []
  if (!historyData.value || historyData.value.length === 0) {
    return
  }

  const getPrice = (day, strategyIndex) => {
    const strategy = priceStrategyOptions[strategyIndex]
    switch (strategy) {
      case '开盘价':
        return day.开盘
      case '收盘价':
        return day.收盘
      case '最高价':
        return day.最高
      case '最低价':
        return day.最低
      case '中间价':
        return (day.最高 + day.最低) / 2
      default:
        return day.收盘 // Default to closing price
    }
  }

  const getBuyQuantity = (capital, price, strategyIndex) => {
    const strategy = buyQuantityStrategyOptions[strategyIndex]
    let capitalToUse = 0
    if (strategy.startsWith('全仓')) capitalToUse = capital
    else if (strategy.startsWith('1/2')) capitalToUse = capital / 2
    else if (strategy.startsWith('1/3')) capitalToUse = capital / 3
    else if (strategy.startsWith('1/4')) capitalToUse = capital / 4
    if (capitalToUse > 0 && price > 0) {
      const numShares = Math.floor(capitalToUse / price / 100) * 100
      return numShares
    }
    return 0
  }

  const getSellQuantity = (shares, strategyIndex) => {
    const strategy = sellQuantityStrategyOptions[strategyIndex]
    if (strategy.startsWith('全仓')) return shares
    if (strategy.startsWith('1/2')) return Math.floor(shares / 2 / 100) * 100
    if (strategy.startsWith('1/3')) return Math.floor(shares / 3 / 100) * 100
    if (strategy.startsWith('1/4')) return Math.floor(shares / 4 / 100) * 100
    return 0
  }

  const initialCapital = capitalOptions[form.value.capital]
  let capital = initialCapital
  let shares = 0
  const transactions: any[] = []

  const signals = props.result.report.reduce((map, signal) => {
    map[signal.index] = signal.trend
    return map
  }, {})

  for (const day of historyData.value) {
    const date = day.日期
    const signal = signals[date]

    if (!signal) {
      continue
    }

    // For now, timing strategies are ignored and considered 'unconditional'

    if (signal === 1 && capital > 0) {
      // Buy Signal
      const price = getPrice(day, form.value.buyPriceStrategy)
      const quantity = getBuyQuantity(capital, price, form.value.buyQuantityStrategy)

      if (quantity > 0) {
        const transactionCost = price * quantity
        const commission = transactionCost * BUY_COMMISSION_RATE
        const capitalChange = -(transactionCost + commission)

        capital += capitalChange
        shares += quantity

        transactions.push({
          index: transactions.length + 1,
          date: date,
          action: '买入',
          price: price.toFixed(2),
          quantity: quantity,
          fee: (-transactionCost).toFixed(2),
          capital: capital.toFixed(2),
          capital_diff: capitalChange.toFixed(2)
        })
      }
    } else if (signal !== 1 && shares > 0) {
      // Sell Signal
      const price = getPrice(day, form.value.sellPriceStrategy)
      const quantity = getSellQuantity(shares, form.value.sellQuantityStrategy)

      if (quantity > 0) {
        const transactionValue = price * quantity
        const commission = transactionValue * SELL_COMMISSION_RATE
        const capitalChange = transactionValue - commission

        capital += capitalChange
        shares -= quantity

        transactions.push({
          index: transactions.length + 1,
          date: date,
          action: '卖出',
          price: price.toFixed(2),
          quantity: quantity,
          fee: transactionValue.toFixed(2),
          capital: capital.toFixed(2),
          capital_diff: `+${capitalChange.toFixed(2)}`
        })
      }
    }
  }

  tableData.value = transactions
}

const handleClose = () => {
  emit('update:visible', false)
  xAxisData.value = []
  chartSeries.value = []
  historyData.value = []
  tableData.value = []
}

watch(
  () => props.visible,
  (val) => {
    if (val && props.stock?.code) {
      apiGetHistoryData({ code: props.stock.code, type: props.stock.type, start: props.dataPeriodStart }).then((res) => {
        if (res.result) {
          historyData.value = res.result
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
            { name: 'MA5', type: 'line', data: calcMAData(5, history.map(item => item.收盘)), symbol: 'none', lineStyle: { width: 1 } },
            { name: 'MA10', type: 'line', data: calcMAData(10, history.map(item => item.收盘)), symbol: 'none', lineStyle: { width: 1 } },
            { name: 'MA15', type: 'line', data: calcMAData(15, history.map(item => item.收盘)), symbol: 'none', lineStyle: { width: 1 } }
          ]

          const volumeSeries = [{ name: 'Volume', type: 'bar', data: volumeData }]

          // Align calculation data with the main history x-axis
          const alignedCalcData = { '日期': xAxisData.value };
          const calcData = props.result.calc;
          if (calcData && calcData['日期']) {
            const calcSeriesKeys = Object.keys(calcData).filter(k => k !== '日期' && k !== 'Signal');
            const calcDataMap = new Map();
            for (let i = 0; i < calcData['日期'].length; i++) {
              const date = calcData['日期'][i];
              const dataPoint = {};
              for (const key of calcSeriesKeys) {
                dataPoint[key] = calcData[key][i];
              }
              calcDataMap.set(date, dataPoint);
            }

            for (const key of calcSeriesKeys) {
              alignedCalcData[key] = [];
            }

            for (const date of xAxisData.value) {
              const calcPoint = calcDataMap.get(date);
              for (const key of calcSeriesKeys) {
                alignedCalcData[key].push(calcPoint?.[key] ?? null);
              }
            }
          }

          const calcSeries = {
            name: 'Calc',
            series: generateCalcChartSeries(props.result, alignedCalcData, props.result.report).seriesData
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
    <el-row :gutter="24">
      <el-col :span="24">
        <div style="height: 250px; display: flex; justify-content: center; margin-bottom: 10px;">
          <Echart v-if="xAxisData.length" :options="chartOptions" :height="'100%'" />
          <div v-else style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center;">Loading chart...</div>
        </div>
      </el-col>
    </el-row>
    <el-divider />
    <el-row :gutter="24">
      <el-col :span="6">
        <el-form :model="form" label-width="120px" ref="formRef">
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
              <el-button type="default" @click="onExecute">回测</el-button>
            </div>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="18">
        <div style="display: flex; flex-direction: column; align-items: center;">
          <el-table :data="tableData" style="width: 90%" :max-height="tableMaxHeight">
            <el-table-column prop="index" label="" width="40" />
            <el-table-column prop="date" label="日期" />
            <el-table-column prop="action" label="操作" width="60" />
            <el-table-column prop="price" label="价格" width="80" />
            <el-table-column prop="quantity" label="数量" width="100" />
            <!-- “费用”更名为“金额”更准确 -->
            <el-table-column prop="fee" label="金额" />
            <el-table-column prop="capital" label="本金" />
            <el-table-column prop="capital_diff" label="差额" />
          </el-table>
          <div style="width: 90%; margin-top: 10px; text-align: right;">
            收益: <b>{{ totalAmount }}</b> &nbsp;&nbsp;&nbsp; 收益率: <b>{{ totalProfitRate }}</b>
          </div>
        </div>
      </el-col>
    </el-row>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="handleClose">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>