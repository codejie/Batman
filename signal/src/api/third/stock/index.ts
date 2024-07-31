import request from '@/axios'
import { NewHighRequest, NewHighResponse } from './types'

export const apiNewHigh = (data: NewHighRequest): Promise<Response<NewHighResponse>> => {
  return request.post({
    url: '/data/third/stock/new_high',
    data
  })
}