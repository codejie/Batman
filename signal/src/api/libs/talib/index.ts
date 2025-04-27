import request from '@/axios'
import { MACDRequest, MACDResult } from './types'

export const apiMACD = (data: MACDRequest): Promise<IResponse<MACDResult>> => {
  return request.post({
    url: '/libs/talib/macd',
    data
  })
}
