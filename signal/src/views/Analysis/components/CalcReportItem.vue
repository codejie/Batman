<script setup lang="ts">
import { computed, ref } from 'vue'
import type { PropType } from 'vue'
import { ElTable, ElTableColumn, ElButton } from 'element-plus'
import { AlgorithmCategoryDefinitions, AlgorithmTypeDefinitions } from '@/api/calc/defines'
import type { AggregatedReport } from './CalcReport.vue'
import { KLineDialog } from '@/components/KLine'
import { FlexChart, SplitChartDialog, type SeriesDataItem } from '@/components/Chart'
import { apiGetHistoryData, type HistoryDataItem } from '@/api/data'

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

const klineDialogVisible = ref<boolean>(false)
const reqParam = ref<any>({})

const chartVisibility = ref<Record<string, boolean>>({})
const splitChartDialogVisible = ref(false)
const selectedRowData = ref<any>(null)
const topChartData = ref<{ seriesData: SeriesDataItem[], xAxisData: string[] }>({ seriesData: [], xAxisData: [] })

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

const calcMAData = (ma: number, data: number[]) => {
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
    result.push(parseFloat((sum / ma).toFixed(2)))
  }
  return result
}

const bottomChartData = computed(() => {
  if (!selectedRowData.value) return { seriesData: [], xAxisData: [] }
  return getChartData(selectedRowData.value.calc, selectedRowData.value.report)
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
  let start_date = new Date()
  if (period === 0) { // 3 months
    start_date.setMonth(end_date.getMonth() - 3)
  } else if (period === 1) { // 6 months
    start_date.setMonth(end_date.getMonth() - 6)
  } else if (period === 2) { // 1 year
    start_date.setFullYear(end_date.getFullYear() - 1)
  } else if (period === 3) { // 2 years
    start_date.setFullYear(end_date.getFullYear() - 2)
  } else {
    start_date.setMonth(end_date.getMonth() - 6) // Default to 6 months
  }
  return start_date.toISOString().slice(0, 10)
}

const openSplitChartDialog = async (row: any) => {
  selectedRowData.value = row
  const startDate = getDateRange(props.dataPeriod)
  const res = await apiGetHistoryData({
    code: props.data.stock.code,
    type: props.data.stock.type,
    start: startDate
  })

  if (res.result) {
    const history = res.result
    const xAxisData = history.map(item => item.日期)
    const klineData = history.map(item => [item.开盘, item.收盘, item.最低, item.最高])
    const closeData = history.map(item => item.收盘)

    const series: SeriesDataItem[] = [
      { name: 'KLine', type: 'candlestick', data: klineData },
      { name: 'MA5', type: 'line', data: calcMAData(5, closeData), symbol: 'none' },
      { name: 'MA10', type: 'line', data: calcMAData(10, closeData), symbol: 'none' },
      { name: 'MA20', type: 'line', data: calcMAData(20, closeData), symbol: 'none' }
    ]
    topChartData.value = { seriesData: series, xAxisData: xAxisData }
  } else {
    topChartData.value = { seriesData: [], xAxisData: [] }
  }

  splitChartDialogVisible.value = true
}

const getChartData = (calcData: any, reportData: any[]): { seriesData: SeriesDataItem[], xAxisData: string[] } => {
  if (!calcData || !calcData['日期']) {
    return { seriesData: [], xAxisData: [] }
  }

  const reportTrendMap = new Map(reportData.map(r => [r.index, r.trend]))
  const xAxisData = calcData['日期']
  const seriesData: SeriesDataItem[] = []

  for (const key in calcData) {
    if (key !== '日期' && key !== 'Signal') {
      const seriesValues = calcData[key]
      const dataPoints = seriesValues.map((value, i) => {
        const date = xAxisData[i]
        if (reportTrendMap.has(date)) {
          const trend = reportTrendMap.get(date)
          return {
            value: value,
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: {
              color: trend === 1 ? '#ec0000' : '#00da3c'
            }
          }
        } else {
          return {
            value: value,
            symbol: 'none'
          }
        }
      })

      seriesData.push({
        name: key,
        type: 'line',
        data: dataPoints
      })
    }
  }
  return { seriesData, xAxisData }
}

const getCategoryTitle = (category: string) => {
  return AlgorithmCategoryDefinitions[category]?.title || category
}

const getTypeTitle = (category: string, type: string) => {
  return AlgorithmTypeDefinitions[category]?.types?.[type]?.title || type
}

const mergedArrayData = computed(() => {
  if (!props.data) {
    return { stock: null, reports: [] };
  }

  if (!props.data.reports || props.data.reports.length === 0) {
    return { stock: props.data.stock, reports: [] };
  }

  const reportGroups = new Map<string, any[]>();

  props.data.reports.forEach(reportInfo => {
    const key = JSON.stringify({
      category: reportInfo.category,
      type: reportInfo.type,
      arguments: reportInfo.arguments
    });

    if (!reportGroups.has(key)) {
      reportGroups.set(key, []);
    }
    reportGroups.get(key)!.push(reportInfo);
  });

  return {
    stock: props.data.stock,
    reports: Array.from(reportGroups.values()).flat()
  };
})

function onTitleClick() {
  reqParam.value = {
    code: props.data.stock.code,
    name: props.data.stock.name,
    type: props.data.stock.type,
  }
  klineDialogVisible.value = true
}
</script>

<template>
  <div class="report-item-container">
    <p class="title" @click="onTitleClick">{{ props.data.stock.name }} ({{ props.data.stock.code }})</p>

    <div v-if="mergedArrayData.reports.length > 0" class="single-report-block">
      
      <el-table :data="mergedArrayData.reports" :border="true" size="small" stripe :show-header="false" default-expand-all>
        <el-table-column type="expand">
          <template #default="{ row }">
            <div v-if="row.report && row.report.length > 0" class="mx-24px my-8px">
              <el-table :data="row.report" :border="true" size="small" stripe>
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
                :series-data="getChartData(row.calc, row.report).seriesData" 
                :x-axis-data="getChartData(row.calc, row.report).xAxisData"
                height="300px"
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
            <div class="title-cell" @click="openSplitChartDialog(row)" style="cursor: pointer;">
              <b>
                <span>
                  {{ getCategoryTitle(row.category) }}: {{ getTypeTitle(row.category, row.type) }}
                  ({{ row.type }})
                  <span v-if="row.arguments">
                    [{{
                      Object.entries(row.arguments)
                        .map(([key, value]) => `${key}=${value}`)
                        .join(', ')
                    }}]
                  </span>
                </span>
              </b>
              <el-button size="small" @click.stop="toggleChart(row)">{{ isChartVisible(row) ? '隐藏图表' : '显示图表' }}</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <KLineDialog :visible="klineDialogVisible" :req-param="reqParam" @update:on-close="klineDialogVisible = false" width="60%" />
    <SplitChartDialog 
      v-if="selectedRowData"
      v-model="splitChartDialogVisible"
      :title="dialogTitle"
      :top-series-data="topChartData.seriesData"
      :bottom-series-data="bottomChartData.seriesData"
      :x-axis-data="topChartData.xAxisData"
    />
  </div>
</template>

<style scoped>
.report-item-container {
  margin-bottom: 16px;
}

.title {
  font-size: 1rem;
  font-weight: bold;
  margin: 0 0 8px 0;
  cursor: pointer;
}

.subtitle {
  font-size: 1rem;
  color: #606266;
  margin: 8px 0;
}

.el-table {
  width: 100%;
}

.single-report-block {
  margin-top: 1rem;
  border: 1px solid #ebeef5;
  padding: 1rem;
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