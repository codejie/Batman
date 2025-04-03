import request from '@/axios'
import { GetLatestHistoryDataRequest, GetLatestHistoryDataResult } from "./types"

export const apiGetLatestHistoryData = (
  data: GetLatestHistoryDataRequest
): Promise<IResponse<GetLatestHistoryDataResult>> => {
  return request.post({
    url: '/data/get_latest_history_data',
    data
  })
}