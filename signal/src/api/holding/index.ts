import request from '@/axios'
import type { CreateRequest, CreateResult, OperationCreateRequest, OperationCreateResult } from './types'
import type { ListRequest, ListResult } from './types'
import type { RecordRequest, RecordResult } from './types'
import type { OperationListRequest, OperationListResult } from './types'
import type { OperationRemoveRequest, OperationRemoveResult } from './types'
import type { FlagRequest, FlagResult } from './types'

export const apiList = (data: ListRequest): Promise<IResponse<ListResult>> => {
  return request.post({ url: '/holding/list', data })
}

export const apiCreate = (data: CreateRequest): Promise<IResponse<CreateResult>> => {
  return request.post({ url: '/holding/create', data })
}

export const apiFlag = (data: FlagRequest): Promise<IResponse<FlagResult>> => {
  return request.post({ url: '/holding/flag', data })
}

export const apiRecord = (data: RecordRequest): Promise<IResponse<RecordResult>> => {
  return request.post({ url: '/holding/record', data })
}

export const apiOperationList = (data: OperationListRequest): Promise<IResponse<OperationListResult>> => {
  return request.post({ url: '/holding/operation/list', data })
}

export const apiOperationCreate = (data: OperationCreateRequest): Promise<IResponse<OperationCreateResult>> => {
  return request.post({ url: '/holding/operation/create', data })
}

export const apiOperationRemove = (data: OperationRemoveRequest): Promise<IResponse<OperationRemoveResult>> => {
  return request.post({ url: '/holding/operation/remove', data })
}