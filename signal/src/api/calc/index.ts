
import request from '@/axios'
import * as Types from './types'

export * from './types'

export const apiCreateAlgorithmItem = (data: Types.CreateAlgorithmItemRequest): Promise<IResponse<Types.CreateAlgorithmItemResult>> => {
  return request.post({ url: '/calc/create', data })
}

export const apiListAlgorithmItems = (data: Types.ListAlgorithmItemsRequest): Promise<IResponse<Types.ListAlgorithmItemsResult>> => {
  return request.post({ url: '/calc/list', data })
}

export const apiDeleteAlgorithmItem = (data: Types.DeleteAlgorithmItemRequest): Promise<IResponse<Types.DeleteAlgorithmItemResult>> => {
  return request.post({ url: '/calc/remove', data })
}

export const apiCreateStockList = (data: Types.CreateStockListRequest): Promise<IResponse<Types.CreateStockListResult>> => {
  return request.post({ url: '/calc/stock_list_create', data })
}

export const apiListStockList = (data: Types.ListStockListRequest): Promise<IResponse<Types.ListStockListResult>> => {
  return request.post({ url: '/calc/stock_list', data })
}

export const apiDeleteStockList = (data: Types.DeleteStockListRequest): Promise<IResponse<Types.DeleteStockListResult>> => {
  return request.post({ url: '/calc/stock_list_remove', data })
}

export const apiCreateArguments = (data: Types.CreateArgumentsRequest): Promise<IResponse<Types.CreateArgumentsResult>> => {
  return request.post({ url: '/calc/arguments_create', data })
}

export const apiListArguments = (data: Types.ListArgumentsRequest): Promise<IResponse<Types.ListArgumentsResult>> => {
  return request.post({ url: '/calc/arguments', data })
}

export const apiDeleteArguments = (data: Types.DeleteArgumentsRequest): Promise<IResponse<Types.DeleteArgumentsResult>> => {
  return request.post({ url: '/calc/arguments_remove', data })
}