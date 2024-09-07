import request from '@/axios'
import * as Stock from './stock/types'
import * as Index from './index/types'

export type HistoryDataModel =  Stock.HistoryDataModel
export type AListModel = Index.AListModel | Stock.AListModel

const TYPE_INDEX: number = 0
const TYPE_STOCK: number = 1

export const apiAList = (type: number = TYPE_STOCK): Promise<Response<Stock.AListResponse | Index.AListResponse>> => {
  return request.post({
    url: type == TYPE_INDEX ? '/data/index/alist' : '/data/stock/alist'
  })
}

export const apiInfo = (data: Stock.InfoRequest | Index.InfoRequest, type: number = TYPE_STOCK): Promise<Response<Stock.InfoResponse | Index.InfoResponse>> => {
  return request.post({
    url: type == TYPE_INDEX ? '/data/index/info' : '/data/stock/info',
    data
  })
} 

export const apiHistory = (data: Stock.HistoryRequest | Index.HistoryRequest, type: number = TYPE_STOCK): Promise<Response<Stock.HistoryResponse | Index.HistoryResponse>> => {
  return request.post({
    url: type == TYPE_INDEX ? '/data/index/history' : '/data/stock/history',
    data
  })
}