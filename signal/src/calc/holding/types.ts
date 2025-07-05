import { HoldingRecordItem, HoldingOperationItem } from "@/api/holding/types"

export interface CalcItem {
  price_avg?: number // 
  date_cur?: string
  price_cur?: number
  revenue?: number
  profit?: number
  profit_rate?: number
  pre_profit?: number,
  pre_profit_rate?: number  
}

export interface HoldingListItem {
  record: HoldingRecordItem
  items?: HoldingOperationItem[]
  calc?: CalcItem
}

export type OperationItem = HoldingOperationItem

// Trace Data

export interface OperationMergedDataItem {
  date: string
  quantity: number // operation quantity
  expense: number
  price: number
  amount: number // expense amount
  holding: number
}

export interface ProfitTraceItem {
  date: string
  holding: number
  amount: number
  quantity: number
  expense: number
  price?: number // 买入
  price_close?: number // 时价
  price_avg?: number
  revenue?: number // 市值
  profit?: number
  profit_rate?: number
  pre_profit?: number,
  pre_profit_rate?: number
  is_filled: boolean
}
