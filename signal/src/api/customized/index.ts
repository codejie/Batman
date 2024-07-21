import request from '@/axios'
import { CreateRequest, CreateResponse, InfosRequest, InfosResponse, RemoveRequest, RemoveResponse } from './types'

export const apiCreate = (data: CreateRequest): Promise<Response<CreateResponse>> => {
  return request.post({
    url: '/customized/create',
    data
  })
}

export const apiInfos = (data: InfosRequest): Promise<Response<InfosResponse>> => {
  return request.post({
    url: '/customized/infos',
    data
  })
}

export const apiRemove = (data: RemoveRequest): Promise<Response<RemoveResponse>> => {
  return request.post({
    url: '/customized/remove',
    data
  })
}