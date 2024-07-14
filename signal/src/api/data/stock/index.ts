import request from '@/axios'
import { HistoryRequest, HistoryResponse } from './types'

export const historyApi = (data: HistoryRequest): Promise<Response<HistoryResponse>> => {
  return request.post({
    url: '/data/stock/history',
    data
  })
}