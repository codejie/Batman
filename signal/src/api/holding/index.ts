import request from '@/axios'
import { CalcHoldingListResponse, CalcHoldingListResquest, CreateRequest, CreateResponse, GetHoldingListRequest, GetHoldingListResponse, GetRecordListResponse, RemoveRequest, RemoveResponse, UpdateRequest, UpdateResponse } from './types'

export const apiCreate = (data: CreateRequest): Promise<Response<CreateResponse>> => {
  return request.post({
    url: '/holding/create',
    data
  })
}

export const apiUpdate = (data: UpdateRequest): Promise<Response<UpdateResponse>> => {
  return request.post({
    url: '/holding/update',
    data
  })
}

export const apiRemove = (data: RemoveRequest): Promise<Response<RemoveResponse>> => {
  return request.post({
    url: '/holding/remove',
    data
  })
}

export const apiGetHoldingList = (data: GetHoldingListRequest): Promise<Response<GetHoldingListResponse>> => {
  return request.post({
    url: '/holding/get_holding',
    data
  })
}

export const apiCetRecordList = (data: GetHoldingListResponse): Promise<Response<GetRecordListResponse>> => {
  return request.post({
    url: '/holding/get_record',
    data
  })
}

export const apiCalcHoldingList = (data: CalcHoldingListResquest): Promise<Response<CalcHoldingListResponse>> => {
  return request.post({
    url: '/holding/calc_holding',
    data
  })
}