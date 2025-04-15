import { apiOperationList, apiRecord } from "@/api/holding"
import { formatDateToYYYYMMDD } from "../comm"
import { OPERATION_ACTION_BUY } from "@/api/holding/types"
import * as Types from "@/calc/holding/types"
import { apiGetLatestHistoryData } from "@/api/data"
import { HistoryData } from "@/api/data/types"
import  { dateUtil, formatToDate } from '@/utils/dateUtil'

export * from "@/calc/holding/types"

// Holding and Operation Data
export async function getHoldingData(id?: number, type?: number, code?: string, flag?: number): Promise<Types.HoldingItem[]> {
  const results: Types.HoldingItem[] = []
  const ret = await apiRecord({
    id,
    type,
    code,
    flag
  })
  for (const item of ret.result) {
    const ret_current = await apiGetLatestHistoryData({
      type: item.type,
      code: item.code
    })
    const price = ret_current.result ? ret_current.result.收盘 : undefined
    const avg = (-item.expense / item.quantity) || undefined
    const precent = price ? ((price * item.quantity + item.expense) / -item.expense) : undefined
    const profit = price ? (price * item.quantity + item.expense) : undefined
    results.push({
      id: item.id,
      type: item.type,
      code: item.code,
      name: item.name,
      flag: item.flag,
      created: item.created,
      updated: item.updated,
      holding: item.quantity,
      expense: item.expense,
      price_avg: avg || undefined,
      price_date: ret_current.result?.日期,
      price_cur: price,
      revenue: price ? price * item.quantity : undefined,
      profit: profit || undefined,
      profit_rate: precent || undefined
    })
  }
  return results
}

export function mergeOperationData(operationData: Types.OperationItem[]): Types.OperationMergedDataItem[] {
  const ret: Types.OperationMergedDataItem[] = []
  let holding: number = 0
  for (const item of operationData) {
    const date = formatDateToYYYYMMDD(item.created)
    const index = ret.findIndex(elment => elment.date === date)
    if (index != -1) {
      ret[index].quantity += ((item.action === OPERATION_ACTION_BUY) ? item.quantity : -item.quantity)
      holding += ret[index].quantity
      ret[index].expense += ((item.action === OPERATION_ACTION_BUY) ? -item.expense : item.expense)
      ret[index].holding = holding
    } else {
      holding += ((item.action === OPERATION_ACTION_BUY) ? item.quantity : -item.quantity)
      ret.push({
        date: date,
        quantity: (item.action === OPERATION_ACTION_BUY) ? item.quantity : -item.quantity,
        expense: (item.action === OPERATION_ACTION_BUY) ? -item.expense : item.expense,
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

  let prev: Types.OperationMergedDataItem | undefined= undefined
  let is_filled = false
  while (start <= end) {
    const date = formatToDate(start)
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
      ret.push({
        ...prev,
        date: date,
        price: price || undefined,
        price_avg: prev.quantity != 0 ? -prev.expense / prev.quantity : undefined,
        revenue: price ? price * prev.quantity : undefined,
        profit: price ? (price * prev.quantity + prev.expense) : undefined,
        profit_rate: price ? ((price * prev.quantity + prev.expense) / -prev.expense) : undefined,
        is_filled
      })      
    }
    start = start.add(1, 'day')
  }
  return ret
}

export function calcProfitTotalData(data: Types.HoldingItem[]): Types.ProfitTotalData{
  let expense = 0
  let revenue = 0
  let profit = 0
  let profit_rate = 0
  for (const item of data) {
    expense += item.expense
    revenue += item.revenue || 0
    profit += item.profit || 0
  }
  profit_rate = profit / -expense
  return {
    expense: expense,
    revenue: revenue,
    profit: profit,
    profit_rate: profit_rate
  }
}

export function calcIntegredData()