<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ContentDetailWrap } from '@/components/ContentDetailWrap'
import { ElButton } from 'element-plus'
import { useTrendStore } from '@/store/modules/calcReport'
import { useTagsView } from '@/hooks/web/useTagsView'
import { useTagsViewStore } from '@/store/modules/tagsView'
import { SplitChart } from '@/components/Chart'
import type { SeriesDataItem } from '@/components/Chart'
import { apiGetHistoryData } from '@/api/data'
import { AlgorithmCategoryDefinitions, AlgorithmTypeDefinitions } from '@/api/calc/defines'

const router = useRouter()
const route = useRoute()
const trendStore = useTrendStore()
const { closeCurrent } = useTagsView()
const tagsViewStore = useTagsViewStore()

const chartId = route.params.id as string
const reportData = computed(() => trendStore.getReportData(chartId))

const chartData = ref<{
  xAxisData: string[]
  series: { name: string; series: SeriesDataItem[] }[]
}>({
  xAxisData: [],
  series: []
})

const calcMAData = (ma: number, data: number[]) => {
  var result: any[] = []
  for (var i = 0, len = data.length; i < len; i++) {
    if (i < ma) {
      result.push('-')
      continue
    }
    var sum = 0
    for (var j = 0; j < ma; j++) {
      sum += +data[i - j]
    }
    result.push(parseFloat((sum / ma).toFixed(2)))
  }
  return result
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

  for (const key in calcData) {
    if (key !== '日期' && key !== 'Signal') {
      const seriesValues = calcData[key]

      seriesData.push({
        name: key,
        type: 'line',
        data: seriesValues,
        showSymbol: false,
        lineStyle: { width: 1 }
      })

      const reportPoints = seriesValues.map((value, i) => {
        const date = xAxisData[i]
        if (reportTrendMap.has(date)) {
          const trend = reportTrendMap.get(date)
          return {
            value: value,
            symbol: 'triangle',
            symbolSize: 8,
            itemStyle: {
              color: trend === 1 ? '#ec0000' : '#00da3c'
            }
          }
        }
        return null
      })

      if (reportPoints.some((p) => p !== null)) {
        seriesData.push({
          name: key + ' Events',
          type: 'line',
          data: reportPoints,
          showSymbol: true,
          lineStyle: {
            opacity: 0
          },
          zlevel: 5,
          large: false
        })
      }
    }
  }
  return { seriesData, xAxisData }
}

watch(
  reportData,
  async (data) => {
    if (data) {
      const res = await apiGetHistoryData({
        code: data.stock.code,
        type: data.stock.type,
        start: data.dataPeriodStart
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

        const klineSeries: SeriesDataItem[] = [
          { name: 'KLine', type: 'candlestick', data: klineData },
          { name: 'MA5', type: 'line', data: calcMAData(5, closeData), symbol: 'none', lineStyle: { width: 1 } },
          { name: 'MA10', type: 'line', data: calcMAData(10, closeData), symbol: 'none', lineStyle: { width: 1 } },
          { name: 'MA20', type: 'line', data: calcMAData(20, closeData), symbol: 'none', lineStyle: { width: 1 } }
        ]

        const volumeSeries: SeriesDataItem[] = [{ name: 'Volume', type: 'bar', data: volumeData }]

        const calcSeries = data.reports
          .filter((report) => report.calc)
          .map((report) => {
            const category = AlgorithmCategoryDefinitions[report.category]?.title || report.category
            const type =
              AlgorithmTypeDefinitions[report.category]?.types?.[report.type]?.title || report.type
            const args = report.arguments
              ? ` (${Object.entries(report.arguments)
                  .map(([k, v]) => `${k}=${v}`)
                  .join(', ')})`
              : ''
            const chartName = `${category}: ${type}${args}`
            return {
              name: chartName,
              series: getCalcChartData(report.calc, report.report).seriesData
            }
          })

        chartData.value = {
          xAxisData,
          series: [{ name: 'K-Line', series: klineSeries }, { name: 'Volume', series: volumeSeries }, ...calcSeries]
        }
      }
    }
  },
  { immediate: true }
)

const chartHeight = computed(() => {
  const numCharts = chartData.value.series.length
  if (numCharts === 0) {
    return '500px'
  }
  const totalWeight = numCharts > 1 ? numCharts + 1 : 2
  const height = Math.ceil((100 * 100 * totalWeight) / (85 * 0.7))
  return `${height}px`
})

const mainChartTitle = computed(() => {
  if (!reportData.value) return ''
  return `${reportData.value.stock.name} (${reportData.value.stock.code})`
})

const title = computed(() => {
  if (!reportData.value) return '聚合图表'
  return `${reportData.value.stock.name} (${reportData.value.stock.code}) - 聚合图表`
})

const goBack = () => {
  router.back()
}

const handleClose = () => {
  closeCurrent()
  const visitedViews = tagsViewStore.getVisitedViews
  const latestView = visitedViews.slice(-1)[0]
  if (latestView) {
    router.push(latestView.fullPath)
  } else {
    router.push('/')
  }
}
</script>

<template>
  <ContentDetailWrap :title="title">
    <template #header>
      <div>
        <ElButton type="primary" @click="goBack">返回</ElButton>
        <ElButton type="danger" @click="handleClose">关闭</ElButton>
      </div>
    </template>
    <div v-if="reportData" class="px-4 pb-4">
      <div class="text-left font-bold text-base py-2">{{ mainChartTitle }}</div>
      <SplitChart
        v-if="chartData.xAxisData.length"
        :x-axis-data="chartData.xAxisData"
        :series="chartData.series"
        :height="chartHeight"
      />
      <div v-else class="p-4 text-center text-gray-500">
        <p>Loading chart data...</p>
      </div>
    </div>
    <div v-else class="p-4 text-center text-gray-500">
      <p>No data available. Please go back and select a report.</p>
    </div>
  </ContentDetailWrap>
</template>