import request from '@/axios'
import * as Types from './types'

export * from './types'

export const apiDownloadList = (data: Types.DownloadListRequest): Promise<IResponse<Types.DownloadListResult>> => {
  return request.post({
    url: '/data/download_list',
    data
  })
}

export const apiGetLatestHistoryData = (
  data: Types.GetLatestHistoryDataRequest
): Promise<IResponse<Types.GetLatestHistoryDataResult>> => {
  return request.post({
    url: '/data/get_latest_history_data',
    data
  })
}

export const apiGetHistoryData = (
  data: Types.GetHistoryDataRequest
): Promise<IResponse<Types.GetHistoryDataResult>> => {
  return request.post({
    url: '/data/get_history_data',
    data
  })
}