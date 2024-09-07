export type AListModel = {
  code: string
  name: string
  market: string
}

export type HistoryDataModel = {
  date: string
  price: number
  percentage: number
  amount: number
  volatility: number
  open: number
  close: number
  high: number
  low: number
  volume: number
  turnover: number
  rate: number  
}

// Request & Response
export type AListResponse = AListModel[]

export type HistoryRequest = {
  code: string
  period?: string
  start?: string
  end?: string
}
export type HistoryResponse = HistoryDataModel[]

export type InfoRequest = {
  code: string
}

export type InfoResponse = AListModel