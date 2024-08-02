import { HistoryDataModel } from '@/api/data/stock/types'
import KLineChart from './src/KLineChart.vue'
import KLineChart2 from './src/KLineChart2.vue'
import KLinePanel from './src/KLinePanel.vue'

export { KLineChart, KLineChart2, KLinePanel }

export type ReqParam = {
  type?: number,
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

export type DataParam = HistoryDataModel[]

// export type ReqParam = {
//   type?: number
//   code: string,
//   name?: string
// }