import { HoldingRecordItem, HoldingOperationItem } from '@/api/holding/types'

export interface CalcItem {
  price_avg?: number //
  date_cur?: string
  price_cur?: number
  revenue?: number
  profit?: number
  profit_rate?: number
  pre_price?: number // 上次收盘价
  pre_price_rate?: number // 上次收盘价变动率
  pre_profit_diff?: number // 盈亏差
  pre_profit_rate?: number
}

export interface HoldingListItem {
  record: HoldingRecordItem
  items?: HoldingOperationItem[]
  calc?: CalcItem
}

export interface SoldoutItem {
  profit: number
  profit_rate: number
  quantity: number
  price: number
  date: Date
}

export interface SoldoutListItem {
  record: HoldingRecordItem
  items?: HoldingOperationItem[]
  calc?: SoldoutItem
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
  pre_profit_diff?: number // 盈亏差
  pre_profit_rate?: number
  is_filled: boolean
}
