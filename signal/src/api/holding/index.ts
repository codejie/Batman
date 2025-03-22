import request from '@/axios'
import type { CreateRequest, CreateResult } from './types'
import type { ListRequest, ListResult } from './types'
import type { RecordRequest, RecordResult } from './types'

export const apiList = (data: ListRequest): Promise<IResponse<ListResult>> => {
  return request.post({ url: '/holding/list', data })
}

export const apiCreate = (data: CreateRequest): Promise<IResponse<CreateResult>> => {
  return request.post({ url: '/holding/create', data })
}

export const apiRecord = (data: RecordRequest): Promise<IResponse<RecordResult>> => {
  return request.post({ url: '/holding/record', data })
}