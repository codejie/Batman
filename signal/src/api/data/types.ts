export const TYPE_INDEX: number = 1
export const TYPE_STOCK: number = 2

export const PERIOD_DAILY: string = 'daily'
export const PERIOD_WEEKLY: string = 'weekly'
export const PERIOD_MONTHLY: string = 'monthly'

export const ADJUST_QFQ: string = 'qfq'

export const RECORD_FLAG_NORMAL: number = 0
export const RECORD_FLAG_DISABLED: number = 1

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

export interface SpotDataItem {
  序号: number
  代码: string
  名称: string
  最新价: number
  涨跌幅: number
  涨跌额: number
  成交量: number
  成交额: number
  振幅: number
  最高: number
  最低: number
  今开: number
  昨收: number
  量比?: number
  换手率?: number
  市盈率?: number
  市净率?: number
  总市值?: number
  流通市值?: number
  涨速?: number
  涨跌5分钟?: number
  涨跌幅60日?: number
  年初至今涨跌幅?: number  
}

export interface GetLatestHistoryDataRequest {
  type: number
  code: string
  period?: string
  adjust?: string
  limit?: number // default 1
  record_flag?: number
}
export type  GetLatestHistoryDataResult = HistoryDataItem | HistoryDataItem[] | undefined

export interface GetHistoryDataRequest {
  type: number
  code: string
  start?: string
  end?: string
  period?: string
  adjust?: string,
  limit?: number,
  record_flag?: number
}
export type GetHistoryDataResult = HistoryDataItem[]

export interface GetSpotDataRequest {
  type: number
  codes?: string[]
  useHistory?: boolean
}
export type GetSpotDataResult = SpotDataItem[]

export interface GetNameRequest {
  type: number
  code: string
}
export type GetNameResult = string

export interface GetItemInfoRequest {
  type: number
  key: string
}
export interface ItemInfo {
  type: number
  code: string
  name: string
}
export type GetItemInfoResult = ItemInfo