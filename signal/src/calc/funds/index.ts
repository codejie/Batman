import { HoldingListItem } from "../holding"
import * as Types  from "./types"

export * from "./types"

export function calcFundsData(funds: Types.FundsItem, holdigns: HoldingListItem[]): Types.FundsData {
  // let total = 0
  let holding = 0
  let expense = 0
  let revenue = 0
  let profit = 0
  // let profit_rate = 0
  for (const item of holdigns) {
    holding += item.record.quantity
    expense += item.record.expense
    revenue += item.calc?.revenue || 0
    profit += item.calc?.profit || 0
  }
  // profit_rate = profit / expense

  const ret = {
    id: funds.id,
    type: funds.type,
    total: revenue + funds.available, //funds.amount + profit,
    amount: funds.amount, // 本金
    holding: holding,
    expense: expense,
    // available: funds.amount + expense,
    available: funds.available,
    revenue: revenue,
    profit: profit,
    profit_rate: (expense === 0 ? undefined : profit / -expense)
  }
  return ret
}