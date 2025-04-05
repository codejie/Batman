import request from '@/axios'
import { GetHistoryDataRequest, GetHistoryDataResult, GetLatestHistoryDataRequest, GetLatestHistoryDataResult } from "./types"

export const apiGetLatestHistoryData = (
  data: GetLatestHistoryDataRequest
): Promise<IResponse<GetLatestHistoryDataResult>> => {
  return request.post({
    url: '/data/get_latest_history_data',
    data
  })
}

export const apiGetHistoryData = (
  data: GetHistoryDataRequest
): Promise<IResponse<GetHistoryDataResult>> => {
  return request.post({
    url: '/data/get_history_data',
    data
  })
}