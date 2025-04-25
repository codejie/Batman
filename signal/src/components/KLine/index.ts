// import { HistoryDataModel } from '@/api/data/stock/types'
// import KLineChart from './src/KLineChart.vue'
import { HistoryDataItem } from '@/api/data'
// import KLineChart2 from './src/KLineChart2.vue'
// import KLineChart3 from './src/KLineChart3.vue'
import KLineChart4 from './src/KLineChart4.vue'
// import KLinePanel from './src/KLinePanel.vue'
import KLinePanel2 from './src/KLinePanel2.vue'

// export { KLineChart, KLineChart2, KLineChart3, KLineChart4, KLinePanel, KLinePanel2 }
export { KLineChart4, KLinePanel2 }

export type ReqParam = {
  type: number,
  code: string,
  name?: string,
  start?: string,
  end?: string,
  period?: string,
  adjust?: string
}

export type ShowParam = {
  maLines: number[],
  markLines?: boolean,
  hideVolume?: boolean,  
  hideKLine?: boolean
}

export type DataParam = HistoryDataItem[]

// export type ReqParam = {
//   type?: number
//   code: string,
//   name?: string
// }