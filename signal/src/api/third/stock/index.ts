import request from '@/axios'
import { NewHighRequest, NewHighResponse } from './types'

export const apiNewHigh = (data: NewHighRequest): Promise<Response<NewHighResponse>> => {
  return request.post({
    url: '/data/third/stock/new_high',
    data
  })
}

export const apiUptrend = (data: UptrendRequest): Promise<Response<UptrendResponse>> => {
  return request.post({
    url: '/data/third/stock/uptrend',
    data
  })
}