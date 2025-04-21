import * as Types from '@/api/funds/types'
import { HoldingListItem } from '../holding'

const FUNDS_STOCK: number = 1
const OPERATION_ACTION_IN: number = 1
const OPERATION_ACTION_OUT: number = 2

export type FundsItem = Types.FundsItem
export type OperationItem = Types.OperationItem

export interface FundsData {
  amount: number // total
  holding: number
  expense: number // 费用
  available: number  
  revenue: number // 市值
  profit: number // 盈亏
  profit_rate: number
}
