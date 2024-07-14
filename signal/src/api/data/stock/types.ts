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
export type HistoryRequest = {
  code: string
  period?: string
  start: string
  end: string
  adjust?: string
}

export type HistoryResponse = HistoryDataModel[]
