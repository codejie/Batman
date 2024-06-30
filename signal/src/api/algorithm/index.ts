import request from '@/axios'
import { InfosRequest, InfosResponse } from './types'

export const apiInfos = (data: InfosRequest): Promise<Response<InfosResponse>> => {
  return request.post({
    url: '/algorithm/infos',
    data
  })
}
