export const TYPE_INDEX: number = 1
export const TYPE_STOCK: number = 2

export const PERIOD_DAILY: string = 'daily'
export const PERIOD_WEEKLY: string = 'weekly'
export const PERIOD_MONTHLY: string = 'monthly'

export const ADJUST_QFQ: string = 'qfq'

export interface DownloadListRequest {
  type: number
}
export type DownloadListResult = void

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
export type  GetLatestHistoryDataResult = HistoryDataItem

export interface GetHistoryDataRequest {
  type: number
  code: string
  start?: string
  end?: string
  period?: string
  adjust?: string  
}
export type GetHistoryDataResult = HistoryDataItem[]