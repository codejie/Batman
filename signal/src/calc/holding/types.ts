import { HoldingRecordItem, HoldingOperationItem } from "@/api/holding/types"

export interface CalcItem {
  price_avg: number // 
  date_cur?: string
  price_cur?: number
  revenue?: number
  profit?: number
  profit_rate?: number
}

export interface HoldingListItem {
  record: HoldingRecordItem
  items: HoldingOperationItem[]
  calc: CalcItem
}

// Holding and Operation Data
// export interface HoldingItem {
//   id: number
//   type: number
//   code: string
//   name: string
//   flag: number
//   created: Date
//   updated: Date
//   holding: number
//   expense: number

//   price_avg?: number
//   price_date?: string
//   price_cur?: number
//   revenue?: number// price_cur * quantity
//   profit?: number// revenue - expense
//   profit_rate?: number
// }

export type OperationItem = HoldingOperationItem

export interface IntegredItem  {
  quantity_rate: number
  expense_rate: number
  revenue_rate: number
}

// Trace Data

export interface OperationMergedDataItem {
  date: string
  quantity: number // operation quantity
  expense: number
  holding: number
}

export interface ProfitTraceItem {
  date: string
  holding: number
  quantity: number
  expense: number
  price?: number
  price_avg?: number
  revenue?: number
  profit?: number
  profit_rate?: number
  is_filled: boolean
}

export interface ProfitTotalData {
  // funds: number,
  // available: number, // 可用funds
  holding: number
  expense: number
  revenue: number //市值
  profit: number
  profit_rate: number
}