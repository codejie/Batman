import { apiOperationList, apiRecord } from "@/api/holding"
import { formatDateToYYYYMMDD } from "../comm"
import * as Types from "@/calc/holding/types"
import { apiGetLatestHistoryData } from "@/api/data"
import { HistoryDataItem } from "@/api/data/types"
import  { dateUtil, formatToDate } from '@/utils/dateUtil'

export * from "@/calc/holding/types"

function _calcPriceAvg(expense: number, quantity: number): number | undefined {
  if (quantity === 0) return 0
  return -expense / quantity
}

function _calcRevenue(quantity: number, price?: number): number | undefined {
  if (price === undefined) return undefined
  return price * quantity
}

function _calcProfit(quantity: number, expense: number, price?: number): number | undefined {
  if (price === undefined) return undefined
  return price * quantity + expense
}

function _calcProfitRate(quantity: number, expense: number, price?: number): number | undefined {
  if (price === undefined) return undefined
  if (expense === 0) return 0
  return (price * quantity + expense) / -expense
}

function _calcPreProfit(profit?: number, pre_profit?: number): number | undefined {
  if (profit === undefined) return undefined
  if (pre_profit === undefined) return undefined
  return profit - pre_profit
}

function _calcPreProfitRate(profit?: number, pre_profit?: number): number | undefined {
  if (profit === undefined) return undefined
  if (pre_profit === undefined) return undefined
  if (pre_profit === 0) return 0
  return (profit - pre_profit) / pre_profit
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
  let amount: number = 0
  for (const item of operationData) {
    const date = formatDateToYYYYMMDD(item.created)
    const index = ret.findIndex(elment => elment.date === date)
    holding += item.quantity
    amount += item.expense  

    if (index != -1) {
      ret[index].quantity += item.quantity
      // holding += ret[index].quantity
      ret[index].expense += item.expense
      // amount += ret[index].expense
      ret[index].price = -ret[index].expense / ret[index].quantity

      ret[index].holding = holding
      ret[index].amount = amount
    } else {
      // holding += item.quantity // ((item.action === OPERATION_ACTION_BUY) ? item.quantity : -item.quantity)
      // amount += item.expense
      ret.push({
        date: date,
        quantity: item.quantity,
        expense: item.expense,
        price: -item.expense / item.quantity,
        amount: amount,
        holding: holding
      })
    }
  }
  return ret
}

export function calcProfitTraceData(operationData: Types.OperationItem[], historyData: HistoryDataItem[]): Types.ProfitTraceItem[] {
  if (operationData.length === 0) {
    return []
  }
  const traceData = mergeOperationData(operationData)
  const ret: Types.ProfitTraceItem[] = []
  let start = dateUtil(traceData[0].date)
  let end = dateUtil(historyData[historyData.length - 1]?.日期)
  if (traceData[traceData.length - 1].holding === 0) {
    end = dateUtil(traceData[traceData.length - 1].date)
  }

  let prev: Types.OperationMergedDataItem | undefined = undefined
  let is_filled = false
  let pre_profit: number | undefined = undefined
  let pre_price: number | undefined = undefined
  while (start <= end) {
    const date = formatToDate(start)
    // console.log('date', date)
    const history = historyData.find(elment => elment.日期 === date)
    if (history) {
      let price = history.收盘
      const item = traceData.find(elment => elment.date === date)
      if (item) {
        prev = item
        is_filled = false
      } else {
        is_filled = true
      }
      if (prev) {
        const profit = _calcProfit(prev.holding, prev.amount, price)
        ret.push({
          ...prev,
          date: date,
          price_close: price || undefined,
          price_avg: _calcPriceAvg(prev.amount, prev.holding), 
          revenue: _calcRevenue(prev.holding, price),
          profit: profit,
          profit_rate: _calcProfitRate(prev.holding, prev.amount, price),
          pre_profit: _calcPreProfit(profit, pre_profit),
          pre_profit_rate: _calcPreProfitRate(profit, pre_profit),
          is_filled
        })
        pre_profit = profit
        pre_price = price    
      }
    }
    start = start.add(1, 'day')
  }
  return ret
}

export function calcProfitData(operationData: Types.OperationItem[], historyData: HistoryDataItem[]): Types.ProfitTraceItem[] {
  if (operationData.length === 0) {
    return []
  }
  const traceData = mergeOperationData(operationData)
  const ret: Types.ProfitTraceItem[] = []
  let pre_price: number | undefined = undefined
  let pre_profit: number | undefined = undefined
  for (const data of traceData) {
    const history = historyData.find(elment => elment.日期 === data.date)
    const price = history ? history.收盘 : undefined
    const profit = _calcProfit(data.holding, data.amount, price)
    ret.push({
      ...data,
      date: data.date,
      price_close: price,
      price_avg: _calcPriceAvg(data.amount, data.holding), 
      revenue: _calcRevenue(data.holding, price),
      profit: profit,
      profit_rate: _calcProfitRate(data.holding, data.amount, price),
      pre_profit: _calcPreProfit(profit, pre_profit),
      pre_profit_rate: _calcPreProfitRate(profit, pre_profit),
      is_filled: false
    })

    pre_price = price
    pre_profit = profit
  }
  return ret  
}
