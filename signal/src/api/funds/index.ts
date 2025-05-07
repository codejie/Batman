import request from '@/axios'
import * as Types from './types'

export * from './types'

// export const apiCreateFunds = (data: Types.CreateRequest): Promise<IResponse<Types.CreateResult>> => {
//   return request.post({ url: '/funds/create', data })
// }

export const apiGetFunds = (data: Types.GetRequest): Promise<IResponse<Types.GetResult>> => {
  return request.post({ url: '/funds/get', data })
}

export const apiUpdateFunds = (data: Types.UpdateRequest): Promise<IResponse<Types.UpdateResult>> => {
  return request.post({ url: '/funds/update', data })
}