import request from '@/axios'
import type { CreateRequest, CreateResponse } from './types'
import type { ListRequest, ListResponse } from './types'

// filepath: /Users/Jie/Code/git/Batman/signal/src/api/holding/index.ts
export const apiList = (data: ListRequest): Promise<IResponse<ListResponse>> => {
  return request.get({ url: '/holding/list', data })
}

export const apiCreate = (data: CreateRequest): Promise<IResponse<CreateResponse>> => {
  return request.post({ url: '/holding/create', data })
}

