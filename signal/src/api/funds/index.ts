import request from '@/axios'
import * as Types from './types'

export * from './types'

export const apiGetFunds = (data: Types.GetRequest): Promise<IResponse<Types.GetResult>> => {
  return request.post({ url: '/funds/get', data })
}