import request from '@/axios'
import * as Types from './types'

export * from './types'

export const apiList = (data: Types.ListRequest): Promise<IResponse<Types.ListResult>> => {
  return request.post({ url: '/holding/list', data })
}

export const apiCreate = (data: Types.CreateRequest): Promise<IResponse<Types.CreateResult>> => {
  return request.post({ url: '/holding/create', data })
}

export const apiFlag = (data: Types.FlagRequest): Promise<IResponse<Types.FlagResult>> => {
  return request.post({ url: '/holding/flag', data })
}

export const apiRecord = (data: Types.RecordRequest): Promise<IResponse<Types.RecordResult>> => {
  return request.post({ url: '/holding/record', data })
}

export const apiOperationList = (
  data: Types.OperationListRequest
): Promise<IResponse<Types.OperationListResult>> => {
  return request.post({ url: '/holding/operation/list', data })
}

export const apiOperationCreate = (
  data: Types.OperationCreateRequest
): Promise<IResponse<Types.OperationCreateResult>> => {
  return request.post({ url: '/holding/operation/create', data })
}

export const apiOperationRemove = (
  data: Types.OperationRemoveRequest
): Promise<IResponse<Types.OperationRemoveResult>> => {
  return request.post({ url: '/holding/operation/remove', data })
}
