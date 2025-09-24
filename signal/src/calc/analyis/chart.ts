import type { SeriesDataItem } from '@/components/Chart'
import { AlgorithmTypeDefinitions } from '@/api/calc/defines'

export const generateCalcChartSeries = (
  report: any,
  calcData: any,
  reportData: any[]
): { seriesData: SeriesDataItem[]; xAxisData: string[] } => {
  if (!calcData || !calcData['日期']) {
    return { seriesData: [], xAxisData: [] }
  }

  const typeDefinition = AlgorithmTypeDefinitions[report.category]?.types?.[report.type]
  const seriesStyle = typeDefinition?.seriesStyle || {}

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

      const style = seriesStyle[key]
      const type = style?.type || 'line'
      let data = seriesValues
      if (type === 'bar' && style?.style === 'macd') {
        data = seriesValues.map((value: number) => ({
          value,
          itemStyle: {
            color: value >= 0 ? '#ec0000' : '#00da3c'
          }
        }))
      }

      seriesData.push({
        name: key,
        type: type,
        data: data,
        showSymbol: false,
        lineStyle: { width: 1 },
        markPoint: markPointData
      })
    }
  }
  return { seriesData, xAxisData }
}

export const calcMAData = (ma: number, data: number[]) => {
  const result: any[] = []
  for (let i = 0, len = data.length; i < len; i++) {
    if (i < ma) {
      result.push('-')
      continue
    }
    let sum = 0
    for (let j = 0; j < ma; j++) {
      sum += +data[i - j]
    }
    result.push(parseFloat((sum / ma).toFixed(2)))
  }
  return result
}

export const alignCalcData = (calcData: any, xAxisData: string[]): any => {
  const fullLength = xAxisData.length
  const calcLength = calcData && calcData['日期'] ? calcData['日期'].length : 0

  if (!calcData || !calcLength || calcLength >= fullLength) {
    return calcData
  }

  const paddedCalcData = {}
  const dateToIndexMap = new Map(xAxisData.map((d, i) => [d, i]))

  for (const key in calcData) {
    if (Object.prototype.hasOwnProperty.call(calcData, key)) {
      paddedCalcData[key] = Array(fullLength).fill(null)
    }
  }
  paddedCalcData['日期'] = [...xAxisData]

  const originalDates = calcData['日期']
  for (let i = 0; i < calcLength; i++) {
    const date = originalDates[i]
    const targetIndex = dateToIndexMap.get(date)
    if (targetIndex !== undefined) {
      for (const key in calcData) {
        if (key !== '日期' && Object.prototype.hasOwnProperty.call(calcData, key)) {
          if (calcData[key] && calcData[key][i] !== undefined) {
            paddedCalcData[key][targetIndex] = calcData[key][i]
          }
        }
      }
    }
  }
  return paddedCalcData
}
