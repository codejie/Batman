import request from '@/axios'
import { CalcHoldingListResponse, CalcHoldingListResquest, CreateRequest, CreateResponse, GetHoldingListRequest, GetHoldingListResponse, GetHoldingRecordRequest, GetHoldingRecordResponse, GetRecordListRequest, GetRecordListResponse, RemoveRecordRequest, RemoveRecordResponse, RemoveRequest, RemoveResponse, UpdateRequest, UpdateResponse } from './types'

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

export const apiRemoveRecord = (data: RemoveRecordRequest): Promise<Response<RemoveRecordResponse>> => {
  return request.post({
    url: '/holding/remove_record',
    data
  })
}

export const apiGetHoldingList = (data: GetHoldingListRequest): Promise<Response<GetHoldingListResponse>> => {
  return request.post({
    url: '/holding/get_holding',
    data
  })
}

export const apiGetRecordList = (data: GetRecordListRequest): Promise<Response<GetRecordListResponse>> => {
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

export const apiGetHoldingRecord = (data: GetHoldingRecordRequest): Promise<Response<GetHoldingRecordResponse>> => {
  return request.post({
    url: '/holding/get_holding_record',
    data
  })
}
