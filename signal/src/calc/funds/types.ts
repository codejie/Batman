import * as Types from '@/api/funds/types'

export const FUNDS_STOCK: number = 1
export const OPERATION_ACTION_IN: number = 1
export const OPERATION_ACTION_OUT: number = 2

export type FundsItem = Types.FundsItem
export type OperationItem = Types.OperationItem

export interface FundsData {
  id: number
  type: number
  total: number // 总额
  amount: number // 本金，资金
  holding: number // 持仓
  expense: number // 费用
  available: number  
  revenue: number // 市值
  profit: number // 盈亏
  profit_rate?: number
}
