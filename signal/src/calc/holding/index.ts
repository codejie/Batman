import { apiOperationList } from "@/api/holding"
import { formatDateToYYYYMMDD } from "../comm"
import { OPERATION_ACTION_BUY } from "@/api/holding/types"
import * as Types from "@/calc/holding/types"
import { apiGetHistoryData } from "@/api/data"

export * from "@/calc/holding/types"

export function getTraceData(holding: number): Promise<Types.TraceDataItem[]> {
  return new Promise((resolve, reject) => {
    const ret: Types.TraceDataItem[] = []
    apiOperationList({ holding })
      .then((res) => {
        for (const item of res.result) {
          const date = formatDateToYYYYMMDD(item.created)
          const index = ret.findIndex(elment => elment.date === date)
          if (index != -1) {
            console.log('quantity', item.quantity, ret[index].quantity, item.action)
            ret[index].quantity += ((item.action === OPERATION_ACTION_BUY) ? item.quantity : -item.quantity)
            console.log('quantity', item.quantity, ret[index].quantity)
            ret[index].expense += ((item.action === OPERATION_ACTION_BUY) ? -item.expense : item.expense)
            console.log('index', index, ret[index])
          } else {
            ret.push({
              date: date,
              quantity: (item.action === OPERATION_ACTION_BUY) ? item.quantity : -item.quantity,
              expense: (item.action === OPERATION_ACTION_BUY) ? -item.expense : item.expense
            })
          }
        }
        resolve(ret)
      })
      .catch((err) => {
        console.error("Error fetching holding trace data:", err)
        reject(err)
      })
  })
}

export async function getProfitTraceData(type: number, code: string, holding?: number): Promise<Types.ProfitTraceItem[]> {
  if (holding === undefined) {
    // holding = await apiGet(type, code)
    holding = 1
  }
  const traceData = await getTraceData(holding)
  if (traceData.length === 0) {
    return []
  }
  const start = traceData[0].date
  const end = traceData[traceData.length - 1].date

  const historyData = await apiGetHistoryData({
    type: type,
    code: code,
    start: start,
    end: end
  })
  console.log('historyData', historyData)
  const ret: Types.ProfitTraceItem[] = []
  for (const item of traceData) {
    console.log('item', item)
    const history = historyData.result.find(elment => elment.日期 === item.date)
    console.log('history', history)
    let price = history ? history.收盘 : undefined
    ret.push({
      ...item,
      price: price || '-',
      price_avg: item.quantity != 0 ? (-item.expense / item.quantity).toFixed(2) : '-',
      revenue: price ? price * item.quantity : '-',
      profit: price ? (price * item.quantity + item.expense) : '-',
      profit_rate: price ? ((price * item.quantity + item.expense) / -item.expense) : '-'
    })
  }
  return ret
}
