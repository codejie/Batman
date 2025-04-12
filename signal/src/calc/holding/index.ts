import { apiOperationList, apiRecord } from "@/api/holding"
import { formatDateToYYYYMMDD } from "../comm"
import { OPERATION_ACTION_BUY } from "@/api/holding/types"
import * as Types from "@/calc/holding/types"
import { apiGetHistoryData, apiGetLatestHistoryData } from "@/api/data"
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
      quantity: item.quantity,
      expense: item.expense,
      price_avg: avg ? avg.toFixed(2) : '-',
      price_date: ret_current.result?.日期,
      price_cur: price || '-',
      revenue: price ? price * item.quantity : '-',
      profit: profit || '-',
      profit_rate: precent ? ((precent * 100).toFixed(2) + '%') : '-'
    })
  }
  return results
}

// Trace Data
export function getTraceData(holding: number): Promise<Types.TraceDataItem[]> {
  return new Promise((resolve, reject) => {
    // const ret: Types.TraceDataItem[] = []
    apiOperationList({ holding })
      .then((res) => {
        const ret = calcTraceData(res.result)
        resolve(ret)
      })
      .catch((err) => {
        console.error("Error fetching holding trace data:", err)
        reject(err)
      })
  })
}

export function calcTraceData(operationData: Types.OperationItem[]): Types.TraceDataItem[] {
  const ret: Types.TraceDataItem[] = []
  for (const item of operationData) {
    const date = formatDateToYYYYMMDD(item.created)
    const index = ret.findIndex(elment => elment.date === date)
    if (index != -1) {
      // console.log('quantity', item.quantity, ret[index].quantity, item.action)
      ret[index].quantity += ((item.action === OPERATION_ACTION_BUY) ? item.quantity : -item.quantity)
      // console.log('quantity', item.quantity, ret[index].quantity)
      ret[index].expense += ((item.action === OPERATION_ACTION_BUY) ? -item.expense : item.expense)
      // console.log('index', index, ret[index])
    } else {
      ret.push({
        date: date,
        quantity: (item.action === OPERATION_ACTION_BUY) ? item.quantity : -item.quantity,
        expense: (item.action === OPERATION_ACTION_BUY) ? -item.expense : item.expense
      })
    }
  }
  return ret
}

export function calcProfitTraceData(operationData: Types.OperationItem[], historyData: HistoryData[]): Types.ProfitTraceItem[] {
  const traceData = calcTraceData(operationData)
  if (traceData.length === 0) {
    return []
  }
  const ret: Types.ProfitTraceItem[] = []
  console.log('historyData', historyData)
  let start = dateUtil(traceData[traceData.length - 1].date)
  console.log('latest', historyData[historyData.length - 1]?.日期)
  const end = dateUtil(historyData[historyData.length - 1]?.日期)

  let prev: Types.TraceDataItem | undefined= undefined
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
        price: price || '-',
        price_avg: prev.quantity != 0 ? (-prev.expense / prev.quantity).toFixed(2) : '-',
        revenue: price ? price * prev.quantity : '-',
        profit: price ? (price * prev.quantity + prev.expense) : '-',
        profit_rate: price ? ((price * prev.quantity + prev.expense) / -prev.expense) : '-',
        is_filled
      })      
    }
    start = start.add(1, 'day')
  }

  // for (const item of traceData) {
  //   const history = historyData.find(elment => elment.日期 === item.date)
  //   let price = history ? history.收盘 : undefined
  //   ret.push({
  //     ...item,
  //     price: price || '-',
  //     price_avg: item.quantity != 0 ? (-item.expense / item.quantity).toFixed(2) : '-',
  //     revenue: price ? price * item.quantity : '-',
  //     profit: price ? (price * item.quantity + item.expense) : '-',
  //     profit_rate: price ? ((price * item.quantity + item.expense) / -item.expense) : '-'
  //   })
  // }

  return ret
}