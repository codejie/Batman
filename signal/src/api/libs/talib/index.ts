import request from '@/axios'
import { MACDRequest, MACDResponse } from './types'

export const apiMACD = (data: MACDRequest): Promise<Response<MACDResponse>> => {
  return request.post({
    url: '/libs/talib/macd',
    data
  })
}
