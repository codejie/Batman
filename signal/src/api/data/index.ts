import request from '@/axios'
import * as Types from './types'

export * from './types'

export const apiDownloadList = (
  data: Types.DownloadListRequest
): Promise<IResponse<Types.DownloadListResult>> => {
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

export const apiGetSpotData = (
  data: Types.GetSpotDataRequest
): Promise<IResponse<Types.GetSpotDataResult>> => {
  return request.post({
    url: '/data/get_spot_data',
    data
  })
}

export const apiGetName = (data: Types.GetNameRequest): Promise<IResponse<Types.GetNameResult>> => {
  return request.post({
    url: '/data/get_name',
    data
  })
}

export const apiGetItemInfo = (
  data: Types.GetItemInfoRequest
): Promise<IResponse<Types.GetItemInfoResult>> => {
  return request.post({
    url: '/data/get_item_info',
    data
  })
}
