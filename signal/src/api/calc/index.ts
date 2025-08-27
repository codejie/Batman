import request from '@/axios'
import * as Types from './types'
import { PATH_URL } from '@/axios/service'
import { useUserStoreWithOut } from '@/store/modules/user'

export * from './types'

export const apiCreateAlgorithmItem = (data: Types.CreateAlgorithmItemRequest): Promise<IResponse<Types.CreateAlgorithmItemResult>> => {
  return request.post({ url: '/calc/create', data })
}

export const apiListAlgorithmItems = (data: Types.ListAlgorithmItemsRequest): Promise<IResponse<Types.ListAlgorithmItemsResult>> => {
  return request.post({ url: '/calc/list', data })
}

export const apiDeleteAlgorithmItem = (data: Types.DeleteAlgorithmItemRequest): Promise<IResponse<Types.DeleteAlgorithmItemResult>> => {
  return request.post({ url: '/calc/remove', data })
}

export const apiGetAlgorithmItem = (data: Types.GetAlgorithmItemRequest): Promise<IResponse<Types.GetAlgorithmItemResult>> => {
  return request.post({ url: '/calc/item', data })
}

export const apiUpdateAlgorithmItem = (data: Types.UpdateAlgorithmItemRequest): Promise<IResponse<Types.UpdateAlgorithmItemResult>> => {
  return request.post({ url: '/calc/update', data })
}

export const apiCreateStockList = (data: Types.CreateStockListRequest): Promise<IResponse<Types.CreateStockListResult>> => {
  return request.post({ url: '/calc/stock_list_create', data })
}

export const apiUpdateStockList = (data: Types.UpdateStockListRequest): Promise<IResponse<Types.UpdateStockListResult>> => {
  return request.post({ url: '/calc/stock_list_update', data })
}

export const apiListStockList = (data: Types.ListStockListRequest): Promise<IResponse<Types.ListStockListResult>> => {
  return request.post({ url: '/calc/stock_list', data })
}

export const apiDeleteStockList = (data: Types.DeleteStockListRequest): Promise<IResponse<Types.DeleteStockListResult>> => {
  return request.post({ url: '/calc/stock_list_remove', data })
}

export const apiCreateArguments = (data: Types.CreateArgumentsRequest): Promise<IResponse<Types.CreateArgumentsResult>> => {
  return request.post({ url: '/calc/arguments_create', data })
}

export const apiUpdateArguments = (data: Types.UpdateArgumentsRequest): Promise<IResponse<Types.UpdateArgumentsResult>> => {
  return request.post({ url: '/calc/arguments_update', data })
}

export const apiListArguments = (data: Types.ListArgumentsRequest): Promise<IResponse<Types.ListArgumentsResult>> => {
  return request.post({ url: '/calc/arguments', data })
}

export const apiDeleteArguments = (data: Types.DeleteArgumentsRequest): Promise<IResponse<Types.DeleteArgumentsResult>> => {
  return request.post({ url: '/calc/arguments_remove', data })
}

export const apiSubmitCalculation = (data: Types.SubmitCalculationRequest): Promise<IResponse<Types.SubmitCalculationResult>> => {
  return request.post({ url: '/calc/submit', data })
}

/**
 * Connects to the SSE endpoint for calculation reports and handles incoming messages.
 * @param onMessage A callback function to execute when a message is received.
 * @param onError A callback function to execute when an error occurs.
 * @returns The EventSource instance, allowing you to close the connection manually.
 */
export const apiConnectToCalcReport = (
  onMessage: (data: Types.CalcReportSseData) => void,
  onError?: (error: Event) => void
): EventSource => {
    const token = useUserStoreWithOut().getTokenKey
  if (!token) {
    console.error('No token found, cannot connect to SSE.')
  }
  const url = `${PATH_URL}/sse/calc_report?token=${token}` // Assuming token is handled by cookies
  console.log('Connecting to SSE URL:', url)
  const eventSource = new EventSource(url, { withCredentials: false })

  eventSource.onmessage = (event) => {
    try {
      // console.log('Received SSE data:', event)
      const parsedData: Types.CalcReportSseData = JSON.parse(event.data)
      console.log('Parsed SSE data:', parsedData)
      onMessage(parsedData)
    } catch (e) {
      console.error('Failed to parse SSE data:', e)
    }
  }

  eventSource.onerror = (error) => {
    console.error('EventSource failed:', error)
    if (onError) {
      onError(error)
    }
    eventSource.close()
  }

    return eventSource
}

export const apiDisconnectFromCalcReport = (eventSource: EventSource | null) => {
  if (eventSource) {
    eventSource.close()
  }
}
