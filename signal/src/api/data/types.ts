export const TYPE_INDEX: number = 1
export const TYPE_STOCK: number = 2

export interface HistoryDataItem {
  日期: string
  开盘: number
  收盘: number
  最高: number
  最低: number
  成交量: number
  成交额: number
  振幅: number
  涨跌幅: number
  涨跌额: number
  换手率: number  
}

export interface GetLatestHistoryDataRequest {
  type: number
  code: string
  period?: string
  adjust?: string
}
export type  GetLatestHistoryDataResult = HistoryDataItem | undefined

export interface GetHistoryDataRequest {
  type: number
  code: string
  start?: string
  end?: string
  period?: string
  adjust?: string  
}
export type GetHistoryDataResult = HistoryDataItem[]