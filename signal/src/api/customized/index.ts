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
  return request.post({ url: '/customized/updateComment', data })
}
