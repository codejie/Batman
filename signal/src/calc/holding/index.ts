import { apiOperationList, apiRecord } from "@/api/holding"
import { formatDateToYYYYMMDD } from "../comm"
import { OPERATION_ACTION_BUY } from "@/api/holding/types"
import * as Types from "@/calc/holding/types"
import { apiGetLatestHistoryData } from "@/api/data"
import { HistoryData } from "@/api/data/types"
import  { dateUtil, formatToDate } from '@/utils/dateUtil'
import { func } from "vue-types"

export * from "@/calc/holding/types"

function _calcPriceAvg(expense: number, quantity: number): number | undefined {
  if (quantity === 0) return undefined
  return -expense / quantity
}

function _calcRevenue(quantity: number, price?: number): number | undefined {
  if (!price) return undefined
  return price * quantity
}

function _calcProfit(quantity: number, expense: number, price?: number): number | undefined {
  if (!price) return undefined
  return price * quantity + expense
}

function _calcProfitRate(quantity: number, expense: number, price?: number): number | undefined {
  if (!price) return undefined
  if (expense === 0) return undefined
  return (price * quantity + expense) / -expense
}

function _calcPreProfit(profit?: number, pre_profit?: number): number | undefined {
  if (!profit) return undefined
  if (!pre_profit) return undefined
  return profit - pre_profit
}

function _calcPreProfitRate(expense: number, profit?: number, pre_profit?: number): number | undefined {
  if (!profit) return undefined
  if (!pre_profit) return undefined
  return (profit - pre_profit) / expense
}

export async function getHoldListData(id?: number, type?: number, code?: string, flag?: number): Promise<Types.HoldingListItem[]> {
  const ret: Types.HoldingListItem[] = []
  const { result } = await apiRecord({
    id,
    type,
    code,
    flag
  })
  
  for (const res of result ) {
    const ret_current = await apiGetLatestHistoryData({
      type: res.type,
      code: res.code
    })
    const price = ret_current.result ? ret_current.result.收盘 : undefined
    const calc: Types.CalcItem = {
      price_avg: _calcPriceAvg(res.expense, res.quantity), // -res.expense / res.quantity,
      price_cur: price,
      date_cur: ret_current.result?.日期,
      revenue: _calcRevenue(res.quantity, price), // price ? price * res.quantity : undefined,
      profit: _calcProfit(res.quantity, res.expense, price), // price ? (price * res.quantity + res.expense) : undefined,
      profit_rate: _calcProfitRate(res.quantity, res.expense, price) // price ? ((price * res.quantity + res.expense) / -res.expense) : undefined
    }
    const ret_opera = await apiOperationList({
      holding: res.id
    })
    const opera = ret_opera.result

    ret.push({
      record: res,
      items: opera,
      calc: calc
    })
  }
  return ret
} 

export function mergeOperationData(operationData: Types.OperationItem[]): Types.OperationMergedDataItem[] {
  const ret: Types.OperationMergedDataItem[] = []
  let holding: number = 0
  for (const item of operationData) {
    const date = formatDateToYYYYMMDD(item.created)
    const index = ret.findIndex(elment => elment.date === date)
    if (index != -1) {
      ret[index].quantity += item.quantity // ((item.action === OPERATION_ACTION_BUY) ? item.quantity : -item.quantity)
      holding += ret[index].quantity

      ret[index].expense += item.expense // ((item.action === OPERATION_ACTION_BUY) ? -item.expense : item.expense)
      ret[index].holding = holding
    } else {
      holding += ((item.action === OPERATION_ACTION_BUY) ? item.quantity : -item.quantity)
      ret.push({
        date: date,
        quantity: item.quantity, //  (item.action === OPERATION_ACTION_BUY) ? item.quantity : -item.quantity,
        expense: item.expense, // (item.action === OPERATION_ACTION_BUY) ? -item.expense : item.expense,
        holding: holding
      })
    }
  }
  return ret
}

export function calcProfitTraceData(operationData: Types.OperationItem[], historyData: HistoryData[]): Types.ProfitTraceItem[] {
  const traceData = mergeOperationData(operationData)
  if (traceData.length === 0) {
    return []
  }
  console.log('traceData', traceData)
  const ret: Types.ProfitTraceItem[] = []
  let start = dateUtil(traceData[0].date)
  let end = dateUtil(historyData[historyData.length - 1]?.日期)
  console.log('holding', traceData[traceData.length - 1].holding)
  if (traceData[traceData.length - 1].holding === 0) {
    end = dateUtil(traceData[traceData.length - 1].date)
  }

  let prev: Types.OperationMergedDataItem | undefined = undefined
  let is_filled = false
  let pre_profit: number | undefined = undefined
  while (start <= end) {
    const date = formatToDate(start)
    console.log('date', date)
    const history = historyData.find(elment => elment.日期 === date)
    let price = history ? history.收盘 : undefined

    const item = traceData.find(elment => elment.date === date)
    if (item) {
      prev = item
      is_filled = false
    } else {
      is_filled = true
    }
    if (prev) {
      const profit = _calcProfit(prev.quantity, prev.expense, price)
      ret.push({
        ...prev,
        date: date,
        price: price || undefined,
        price_avg: _calcPriceAvg(prev.expense, prev.quantity), // prev.quantity != 0 ? -prev.expense / prev.quantity : undefined,
        revenue: _calcRevenue(prev.quantity, price), // price ? price * prev.quantity : undefined,
        profit: profit, // _calcProfit(prev.quantity, prev.expense, price), // price ? (price * prev.quantity + prev.expense) : undefined,
        profit_rate: _calcProfitRate(prev.quantity, prev.expense, price), // price ? ((price * prev.quantity + prev.expense) / prev.expense) : undefined,
        pre_profit: _calcPreProfit(profit, pre_profit),
        pre_profit_rate: _calcPreProfitRate(prev.expense, profit, pre_profit),
        is_filled
      })
      pre_profit = profit    
    }
    start = start.add(1, 'day')
  }
  return ret
}

export function calcProfitTotalData(data: Types.HoldingListItem[]): Types.ProfitTotalData{
  let holding
  let expense = 0
  let revenue = 0
  let profit = 0
  let profit_rate = 0
  for (const item of data) {
    holding += item.record.quantity
    expense += item.record.expense
    revenue += item.calc.revenue || 0
    profit += item.calc.profit || 0
  }
  profit_rate = profit / expense
  return {
    holding: holding,
    expense: expense,
    revenue: revenue,
    profit: profit,
    profit_rate: profit_rate
  }
}
