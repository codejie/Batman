<script setup lang="ts">
import { computed, ref } from 'vue'
import type { PropType } from 'vue'
import { ElTable, ElTableColumn, ElButton } from 'element-plus'
import { useTrendStore, ReportData } from '@/store/modules/calcReport'
import { useRouter } from 'vue-router'
import { AlgorithmCategoryDefinitions, AlgorithmTypeDefinitions } from '@/api/calc/defines'
import type { AggregatedReport } from './CalcReport.vue'
import { KLineDialog } from '@/components/KLine'
import { FlexChart, TripleChartDialog, type SeriesDataItem } from '@/components/Chart'
import { apiGetHistoryData } from '@/api/data'
import CalcReportBackTestDialog from './CalcReportBackTestDialog.vue'
import { generateCalcChartSeries,calcMAData } from '@/calc/analyis/chart'

const props = defineProps({
  data: {
    type: Object as PropType<AggregatedReport>,
    required: true
  },
  dataPeriod: {
    type: Number,
    required: true
  }
})

const router = useRouter()
const trendStore = useTrendStore()

const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<any>({})

const chartVisibility = ref<Record<string, boolean>>({})
const tripleChartDialogVisible = ref(false)
const selectedRowData = ref<any>(null)
const topChartData = ref<{ seriesData: SeriesDataItem[]; xAxisData: string[] }>({
  seriesData: [],
  xAxisData: []
})

const selectedReportForBacktest = ref(null)
const isBacktestDialogVisible = ref(false)

const onBacktestClick = (row: any) => {
  selectedReportForBacktest.value = row
  isBacktestDialogVisible.value = true
}

const get_row_key = (row: any) => {
  return `${row.category}-${row.type}-${JSON.stringify(row.arguments)}`
}

const isChartVisible = (row: any) => {
  return chartVisibility.value[get_row_key(row)] || false
}

const toggleChart = (row: any) => {
  const key = get_row_key(row)
  chartVisibility.value[key] = !isChartVisible(row)
}


const bottomChartData = computed(() => {
  if (!selectedRowData.value) return { seriesData: [], xAxisData: [] }
  return generateCalcChartSeries(
    selectedRowData.value,
    selectedRowData.value.calc,
    selectedRowData.value.report
  )
})

const dialogTitle = computed(() => {
  if (!selectedRowData.value) return ''
  const stock = props.data.stock
  const row = selectedRowData.value
  const category = getCategoryTitle(row.category)
  const type = getTypeTitle(row.category, row.type)
  return `${stock.name}(${stock.code}) - ${category}: ${type} (${row.type})`
})

const getDateRange = (period: number): string => {
  const end_date = new Date()
  const start_date = new Date()
  if (period === 0) {
    // 3 months
    start_date.setMonth(end_date.getMonth() - 3)
  } else if (period === 1) {
    // 6 months
    start_date.setMonth(end_date.getMonth() - 6)
  } else if (period === 2) {
    // 1 year
    start_date.setFullYear(end_date.getFullYear() - 1)
  } else if (period === 3) {
    // 2 years
    start_date.setFullYear(end_date.getFullYear() - 2)
  } else {
    start_date.setMonth(end_date.getMonth() - 6) // Default to 6 months
  }
  return start_date.toISOString().slice(0, 10)
}

const middleChartData = ref<{ seriesData: SeriesDataItem[] }>({ seriesData: [] })

const dataPeriodStart = ref<string>(getDateRange(props.dataPeriod))

const openTripleChartDialog = async (row: any) => {
  selectedRowData.value = row
  // const startDate = getDateRange(props.dataPeriod)
  const res = await apiGetHistoryData({
    code: props.data.stock.code,
    type: props.data.stock.type,
    start: dataPeriodStart.value
  })

  if (res.result) {
    const history = res.result
    const xAxisData = history.map((item) => item.日期)
    const klineData = history.map((item) => [item.开盘, item.收盘, item.最低, item.最高])
    const closeData = history.map((item) => item.收盘)
    const volumeData = history.map((item, index) => {
      const open = history[index].开盘
      const close = history[index].收盘
      return {
        value: item.成交量,
        itemStyle: {
          color: close >= open ? '#ec0000' : '#00da3c'
        }
      }
    })

    const topSeries: SeriesDataItem[] = [
      { name: 'KLine', type: 'candlestick', data: klineData },
      { name: 'MA5', type: 'line', data: calcMAData(5, closeData), symbol: 'none' },
      { name: 'MA10', type: 'line', data: calcMAData(10, closeData), symbol: 'none' },
      { name: 'MA20', type: 'line', data: calcMAData(20, closeData), symbol: 'none' }
    ]
    topChartData.value = { seriesData: topSeries, xAxisData: xAxisData }

    const middleSeries: SeriesDataItem[] = [{ name: 'Volume', type: 'bar', data: volumeData }]
    middleChartData.value = { seriesData: middleSeries }
  } else {
    topChartData.value = { seriesData: [], xAxisData: [] }
    middleChartData.value = { seriesData: [] }
  }

  tripleChartDialogVisible.value = true
}



const getCategoryTitle = (category: string) => {
  const title = AlgorithmCategoryDefinitions[category]?.title || category
  return `${title}(${category})`
}

const getTypeTitle = (category: string, type: string) => {
  return AlgorithmTypeDefinitions[category]?.types?.[type]?.title || type
}

const mergedArrayData = computed(() => {
  if (!props.data) {
    return { stock: null, reports: [] }
  }

  if (!props.data.reports || props.data.reports.length === 0) {
    return { stock: props.data.stock, reports: [] }
  }

  const reportGroups = new Map<string, any[]>()

  props.data.reports.forEach((reportInfo) => {
    const key = JSON.stringify({
      category: reportInfo.category,
      type: reportInfo.type,
      arguments: reportInfo.arguments
    })

    if (!reportGroups.has(key)) {
      reportGroups.set(key, [])
    }
    reportGroups.get(key)!.push(reportInfo)
  })

  return {
    stock: props.data.stock,
    reports: Array.from(reportGroups.values()).flat()
  }
})

const hasCalcData = computed(() => {
  return props.data?.reports?.some((report) => !!report.calc)
})

const navigateToTrendChart = () => {
  const uniqueId = `${props.data.stock.code}_${Date.now()}`
  const reportDataWithPeriod: ReportData = {
    ...props.data,
    dataPeriodStart: dataPeriodStart.value
  }
  trendStore.setReportData(uniqueId, reportDataWithPeriod)
  router.push({ name: 'TrendReportChart', params: { id: uniqueId } })
}

function onTitleClick() {
  reqParam.value = {
    code: props.data.stock.code,
    name: props.data.stock.name,
    type: props.data.stock.type
  }
  klineDialogVisible.value = true
}
</script>

<template>
  <div class="report-item-container">
    <div class="title-container">
      <p class="title" @click="onTitleClick"
        >{{ props.data.stock.name }} ({{ props.data.stock.code }})</p
      >
      <el-button
        v-if="hasCalcData"
        size="default"
        @click="navigateToTrendChart"
        style="margin-left: 1rem"
        >聚合图表</el-button
      >
    </div>

    <div v-if="mergedArrayData.reports.length > 0" class="single-report-block">
      <el-table
        :data="mergedArrayData.reports"
        :border="true"
        size="small"
        stripe
        :show-header="false"
        default-expand-all
      >
        <el-table-column type="expand">
          <template #default="{ row }">
            <div v-if="row.report && row.report.length > 0" class="mx-24px my-8px">
              <el-table :data="row.report" :border="true" size="small" stripe>
                <el-table-column label="序号" width="60" align="center">
                  <template #default="scope"> ({{ scope.$index + 1 }}) </template>
                </el-table-column>
                <el-table-column prop="index" label="日期" />
                <el-table-column prop="trend" label="趋势信号">
                  <template #default="{ row: innerRow }">
                    <span v-if="innerRow.trend === 1" style="color: red">上涨</span>
                    <span v-else-if="innerRow.trend === -1" style="color: green">下跌</span>
                    <span v-else-if="innerRow.trend === 0" style="color: grey">--</span>
                  </template>
                </el-table-column>
                <el-table-column prop="price" label="价格" />
              </el-table>
            </div>
            <div v-if="isChartVisible(row) && row.calc" class="chart-container">
              <FlexChart
                :key="get_row_key(row)"
                :series-data="generateCalcChartSeries(row, row.calc, row.report).seriesData"
                :x-axis-data="generateCalcChartSeries(row, row.calc, row.report).xAxisData"
                height="200px"
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="Index" width="60">
          <template #default="scope">
            <b>{{ scope.$index + 1 }}</b>
          </template>
        </el-table-column>
        <el-table-column label="Title">
          <template #default="{ row }">
            <div
              class="title-cell"
              :style="row.calc ? 'cursor: pointer;' : ''"
              @click="row.calc && openTripleChartDialog(row)"
            >
              <b>
                <span>
                  {{ getCategoryTitle(row.category) }}:
                  {{ getTypeTitle(row.category, row.type) }} ({{ row.type }})
                  <span v-if="row.arguments">
                    [{{
                      Object.entries(row.arguments)
                        .map(([key, value]) => `${key}=${value}`)
                        .join(', ')
                    }}]
                  </span>
                </span>
              </b>
              <div>
                <el-button size="small" v-if="row.calc" @click.stop="onBacktestClick(row)">模拟回测</el-button>
                <el-button size="small" v-if="row.calc" @click.stop="toggleChart(row)">{{
                  isChartVisible(row) ? '隐藏图表' : '显示图表'
                }}</el-button>
              </div>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <KLineDialog
      :visible="klineDialogVisible"
      :req-param="reqParam"
      @update:on-close="klineDialogVisible = false"
      width="60%"
    />
    <TripleChartDialog
      v-if="selectedRowData"
      v-model="tripleChartDialogVisible"
      :title="dialogTitle"
      :top-series-data="topChartData.seriesData"
      :middle-series-data="middleChartData.seriesData"
      :bottom-series-data="bottomChartData.seriesData"
      :x-axis-data="topChartData.xAxisData"
    />
    <CalcReportBackTestDialog v-if="selectedReportForBacktest" v-model:visible="isBacktestDialogVisible" :stock="props.data.stock" :result="selectedReportForBacktest" :dataPeriodStart="dataPeriodStart" />
  </div>
</template>

<style scoped>
.report-item-container {
  margin-bottom: 16px;
}

.title-container {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.title {
  margin: 0;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
}

.subtitle {
  margin: 8px 0;
  font-size: 1rem;
  color: #606266;
}

.el-table {
  width: 100%;
}

.single-report-block {
  padding: 1rem;
  margin-top: 1rem;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

.title-cell {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.chart-container {
  margin-top: 1rem;
}
</style>
