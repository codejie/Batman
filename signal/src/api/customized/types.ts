export interface CreateRequest {
  type: number
  code: string
  comment?: string
}
export type CreateResult = number

export interface RecordsRequest {
  type?: number
  code?: string
}
export type RecordsItem = {
  id: number
  type: number
  code: string
  name: string
  target: number
  order: number
  comment?: string
  updateTime: string
  holding?: number
}

export interface RemoveRequest {
  id: number
}
export type RemoveResult = number

export interface UpdateCommentRequest {
  id: number
  comment?: string
}
export type UpdateCommentResult = number

export interface UpdateTargetRequest {
  id: number
  target: number
}
export type UpdateTargetResult = number

export interface UpdateOrderRequest {
  id: number
  order: number
}
export type UpdateOrderResult = number