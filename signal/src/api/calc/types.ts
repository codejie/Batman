export interface AlgorithmItem {
  id?: number
  uid?: number
  name: string
  remarks?: string
  category: number
  type: number
  list_type: number
  data_period: number
  report_period: number
  created: Date
}

export interface StockListItem {
  id: number
  cid: number
  type: number
  code: string
}

export interface ArgumentItem {
  id: number
  cid: number
  category: number
  type: number
  arguments: string
  flag: number
}

// Requests and Results
export interface CreateAlgorithmItemRequest {
  name: string
  category: number
  type: number
  list_type: number
  data_period: number
  report_period: number
  remarks?: string
}
export type CreateAlgorithmItemResult = number

export interface ListAlgorithmItemsRequest {}
export type ListAlgorithmItemsResult = AlgorithmItem[]

export interface DeleteAlgorithmItemRequest {
  id: number
}
export type DeleteAlgorithmItemResult = number

export interface CreateStockListRequest {
  cid: number
  items: StockListItem[]
}
export type CreateStockListResult = number

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

export interface ListArgumentsRequest {
  cid: number
}
export type ListArgumentsResult = ArgumentItem[]

export interface DeleteArgumentsRequest {
  cid: number
  id?: number
}
export type DeleteArgumentsResult = number
