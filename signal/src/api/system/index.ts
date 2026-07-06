import axios from 'axios'
import request from '@/axios'
import {
  DbExportRequest,
  DbImportRequest,
  DbImportResult,
  DbRemoveAllHistoryDataRequest,
  DbRemoveAllHistoryDataResult,
  DataConfigGetRequest,
  DataConfigGetResult,
  DataConfigSaveRequest,
  DataConfigSaveResult,
  TradeCalendarGetRequest,
  TradeCalendarGetResult,
  TradeCalendarSaveRequest,
  TradeCalendarSaveResult
} from './types'
import { PATH_URL } from '@/axios/service'

export const apiDbExport = (data: DbExportRequest) => {
  // return request.get({ url: '/system/db/export', data, responseType: 'blob' })

  axios({
    baseURL: PATH_URL,
    url: '/system/db/export',
    method: 'POST',
    responseType: 'blob', // 表示服务器响应的数据类型
    data
  })
    .then((response) => {
      // 尝试从Content-Disposition头中获取文件名
      const contentDisposition = response.headers['content-disposition']
      let filename = 'export.zip'
      if (contentDisposition) {
        const matches = contentDisposition.match(/filename="([^"]+)"/)
        if (matches.length === 2) {
          filename = matches[1]
        }
      }

      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.parentNode?.removeChild(link)
    })
    .catch((error) => {
      console.error(error)
    })
}

export const urlDbImport = `${PATH_URL}/system/db/import`

export const apiDbImport = (data: DbImportRequest): Promise<IResponse<DbImportResult>> => {
  return request.post({ url: '/system/db/import', data })
}

export const apiDbRemoveAllHistoryData = (
  data: DbRemoveAllHistoryDataRequest
): Promise<IResponse<DbRemoveAllHistoryDataResult>> => {
  return request.post({ url: '/data/remove_history_data', data })
}

export const apiGetTradeCalendar = (
  data: TradeCalendarGetRequest
): Promise<IResponse<TradeCalendarGetResult>> => {
  return request.post({ url: '/system/trade_calendar/get', data })
}

export const apiSaveTradeCalendar = (
  data: TradeCalendarSaveRequest
): Promise<IResponse<TradeCalendarSaveResult>> => {
  return request.post({ url: '/system/trade_calendar/save', data })
}

export const apiGetDataConfig = (
  data: DataConfigGetRequest
): Promise<IResponse<DataConfigGetResult>> => {
  return request.post({ url: '/system/data_config/get', data })
}

export const apiSaveDataConfig = (
  data: DataConfigSaveRequest
): Promise<IResponse<DataConfigSaveResult>> => {
  return request.post({ url: '/system/data_config/save', data })
}
