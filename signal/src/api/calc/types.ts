
export interface AlgorithmItem {
  id?: number
  uid?: number
  name: string
  remarks?: string
  list_type: number
  data_period: number
  report_period: number
  show_opt: number
  created: Date
}

export interface StockListItem {
  id?: number
  cid?: number
  type: number
  code: string
  name?: string
}

export interface ArgumentItem {
  id?: number
  cid: number
  category: string
  type: string
  arguments: string
  flag?: number
}

// Requests and Results
export interface CreateAlgorithmItemRequest {
  name: string
  list_type: number
  data_period: number
  report_period: number
  show_opt?: number
  remarks?: string
}
export type CreateAlgorithmItemResult = number

export interface ListAlgorithmItemsRequest {}
export type ListAlgorithmItemsResult = AlgorithmItem[]

export interface DeleteAlgorithmItemRequest {
  id: number
}
export type DeleteAlgorithmItemResult = number

export interface GetAlgorithmItemRequest {
  id: number
}
export type GetAlgorithmItemResult = AlgorithmItem | null

export interface UpdateAlgorithmItemRequest {
  id: number
  name: string
  list_type: number
  data_period: number
  report_period: number
  show_opt: number
  remarks?: string
}
export type UpdateAlgorithmItemResult = number

export interface CreateStockListRequest {
  cid: number
  items: StockListItem[]
}
export type CreateStockListResult = number

export interface UpdateStockListRequest {
  cid: number
  items: StockListItem[]
}
export type UpdateStockListResult = number

export interface ListStockListRequest {
  cid: number
}
export type ListStockListResult = StockListItem[]

export interface DeleteStockListRequest {
  cid: number
  id?: number
}
export type DeleteStockListResult = number

export interface CreateArgumentsRequest {
  cid: number
  items: ArgumentItem[]
}
export type CreateArgumentsResult = number

export interface UpdateArgumentsRequest {
  cid: number
  items: ArgumentItem[]
}
export type UpdateArgumentsResult = number

export interface ListArgumentsRequest {
  cid: number
}
export type ListArgumentsResult = ArgumentItem[]

export interface DeleteArgumentsRequest {
  cid: number
  id?: number
}
export type DeleteArgumentsResult = number

export interface SubmitCalculationRequest {
  id: number
}
export type SubmitCalculationResult = number

// SSE Payloads
export interface CalcResultType {
  calc: any
  report: any
}
export interface CalcReportData {
  category: string
  type: string
  stock: {
    type: number
    code: string
    name: string
  }
  result: CalcResultType
  arguments: any
}

export interface SsePayload<T> {
  code: number
  message: string | null
  type: string
  data: T | null
}

export type CalcReportTrendReportType = {
  index: string
  price: number
  trend: number
}

// Connecting to SSE...
// {
//   "catagory": 0,
//   "type": 0,
//   "stock": {
//     "type": 2,
//     "code": "000001",
//     "name": "平安银行"
//   },
//   "report": [
//     {
//       "index": "2025-05-07",
//       "price": 10.67,
//       "trend": 1
//     },
//     {
//       "index": "2025-07-23",
//       "price": 12.53,
//       "trend": -1
//     }
//   ]
// }