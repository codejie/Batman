import { HoldingOperationItem } from "@/api/holding/types"

// Holding and Operation Data
export interface HoldingItem {
  id: number
  type: number
  code: string
  name: string
  flag: number
  created: Date
  updated: Date
  quantity: number
  expense: number

  price_avg: number | string
  price_date?: string
  price_cur?: number | string
  revenue?: number | string// price_cur * quantity
  profit?: number | string// revenue - expense
  profit_rate?: number | string
}

export type OperationItem = HoldingOperationItem
// export interface OperationItem {
//   id: number
//   holding: number
//   action: number
//   quantity: number
//   price: number
//   expense: number
//   comment?: string
//   created: Date
// }

// Trace Data

export interface TraceDataItem {
  date: string
  quantity: number
  expense: number
}

export interface ProfitTraceItem {
  date: string
  quantity: number
  expense: number
  price: number | string
  price_avg: number | string
  revenue: number | string
  profit: number | string
  profit_rate: number | string
}

