import request from '@/axios'
import {
  CreateInstanceRequest,
  CreateInstanceResponse,
  GetInstanceRequest,
  GetInstanceResponse,
  InfosRequest,
  InfosResponse,
  ListInstanceRequest,
  ListInstanceResponse,
  RemoveInstanceRequest,
  RemoveInstanceResponse,
  ResetInstanceRequest,
  ResetInstanceResponse
} from './types'

export const apiInfos = (data: InfosRequest): Promise<Response<InfosResponse>> => {
  return request.post({
    url: '/strategy/infos',
    data
  })
}

export const apiList = (data: ListInstanceRequest): Promise<Response<ListInstanceResponse>> => {
  return request.post({
    url: '/strategy/list',
    data
  })
}

export const apiGet = (data: GetInstanceRequest): Promise<Response<GetInstanceResponse>> => {
  return request.post({
    url: '/strategy/get',
    data
  })
}

export const apiRemove = (
  data: RemoveInstanceRequest
): Promise<Response<RemoveInstanceResponse>> => {
  return request.post({
    url: '/strategy/remove',
    data
  })
}

export const apiCreate = (
  data: CreateInstanceRequest
): Promise<Response<CreateInstanceResponse>> => {
  return request.post({
    url: '/strategy/create',
    data
  })
}

export const apiReset = (
  data: ResetInstanceRequest
): Promise<Response<ResetInstanceResponse>> => {
  return request.post({
    url: '/strategy/reset',
    data
  })
}
