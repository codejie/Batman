import request from '@/axios'
import { ListInstanceRequest, ListInstanceResponse, RemoveInstanceRequest, RemoveInstanceResponse } from './types'

export const apiList = (data: ListInstanceRequest): Promise<Response<ListInstanceResponse>> => {
    return request.post({
        url: '/strategy/list',
        data
    })
}

export const apiRemove = (data: RemoveInstanceRequest): Promise<Response<RemoveInstanceResponse>> => {
    return request.post({
        url: '/strategy/remove',
        data
    })
}