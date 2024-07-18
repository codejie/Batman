import request from '@/axios'
import { CreateRequest, CreateResponse } from './types'

export const apiCreate = (data: CreateRequest): Promise<Response<CreateResponse>> => {
  return request.post({
    url: '/customized/create',
    data
  })
}