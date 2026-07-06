export interface DbExportRequest {
  flag?: number
}

export type DbExportResult = {
  path: string
  filename: string
  media_type: string
}

export interface DbImportRequest {}
export type DbImportResult = number

export interface DbRemoveAllHistoryDataRequest {}
export type DbRemoveAllHistoryDataResult = number

export interface TradeCalendarGetRequest {
  year: number
}

export interface TradeCalendarData {
  year: number
  trade_days: string[]
  non_trade_days: string[]
  source: 'default' | 'saved'
}

export type TradeCalendarGetResult = TradeCalendarData

export interface TradeCalendarSaveRequest {
  year: number
  trade_days: string[]
  non_trade_days: string[]
}

export type TradeCalendarSaveResult = TradeCalendarData

export type MarketDataSource = 'akshare' | 'tencent'

export interface DataConfigGetRequest {}

export interface DataConfigData {
  market_data_source: MarketDataSource
}

export type DataConfigGetResult = DataConfigData

export interface DataConfigSaveRequest {
  market_data_source: MarketDataSource
}

export type DataConfigSaveResult = DataConfigData
