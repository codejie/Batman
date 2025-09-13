import { HistoryDataItem, SpotDataItem } from '@/api/data'
import { CustomizedCalcItem } from './types'

export * from './types'

// export function calcCustomizedData(data: HistoryDataItem): CustomizedCalcItem | undefined {
//   if (!data) {
//     return undefined
//   }
//   return {
//     price: data.收盘,
//     date: data.日期,
//     price_change: data.涨跌额,
//     price_change_rate: data.涨跌幅
//   }
// }

export function calcCustomizedData(data?: SpotDataItem): CustomizedCalcItem | undefined {
  if (!data) {
    return undefined
  }
  return data
}
