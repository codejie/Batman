// types.ts
export interface SeriesDataItem {
  name: string
  type: 'line' | 'bar' | 'candlestick'
  data: any[]
  // Allow any other echarts series properties
  [key: string]: any
}
