import request from '@/axios'
import * as Types from './types'

export * from './types'

export const apiCreate = (data: Types.CreateRequest): Promise<IResponse<Types.CreateResult>> => {
  return request.post({ url: '/customized/create', data })
}

export const apiRecords = (data: Types.RecordsRequest): Promise<IResponse<Types.RecordsItem[]>> => {
  return request.post({ url: '/customized/records', data })
}

export const apiRemove = (data: Types.RemoveRequest): Promise<IResponse<Types.RemoveResult>> => {
  return request.post({ url: '/customized/remove', data })
}

export const apiUpdateComment = (data: Types.UpdateCommentRequest): Promise<IResponse<Types.UpdateCommentResult>> => {
  return request.post({ url: '/customized/update_comment', data })
}

export const apiUpdateTarget = (data: Types.UpdateTargetRequest): Promise<IResponse<Types.UpdateTargetResult>> => {
  return request.post({ url: '/customized/update_target', data })
}

export const apiUpdateOrder = (data: Types.UpdateOrderRequest): Promise<IResponse<Types.UpdateOrderResult>> => {
  return request.post({ url: '/customized/update_order', data })
}
