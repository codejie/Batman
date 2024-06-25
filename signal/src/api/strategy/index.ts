import request from '@/axios'
import {
  InfosRequest,
  InfosResponse,
  ListInstanceRequest,
  ListInstanceResponse,
  RemoveInstanceRequest,
  RemoveInstanceResponse
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

export const apiRemove = (
  data: RemoveInstanceRequest
): Promise<Response<RemoveInstanceResponse>> => {
  return request.post({
    url: '/strategy/remove',
    data
  })
}
