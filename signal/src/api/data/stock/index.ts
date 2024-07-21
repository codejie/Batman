import request from '@/axios'
import { AListResponse, HistoryRequest, HistoryResponse } from './types'

export const apiAList = (): Promise<Response<AListResponse>> => {
  return request.post({
    url: '/data/stock/alist'
  })
}
export const apiHistory = (data: HistoryRequest): Promise<Response<HistoryResponse>> => {
  return request.post({
    url: '/data/stock/history',
    data
  })
}