import request from '@/axios'
import { AListResponse, HistoryRequest, HistoryResponse, InfoRequest, InfoResponse } from './types'

export const apiAList = (): Promise<Response<AListResponse>> => {
  return request.post({
    url: '/data/stock/alist'
  })
}

export const apiInfo = (data: InfoRequest): Promise<Response<InfoResponse>> => {
  return request.post({
    url: '/data/stock/info',
    data
  })
} 

export const apiHistory = (data: HistoryRequest): Promise<Response<HistoryResponse>> => {
  return request.post({
    url: '/data/stock/history',
    data
  })
}