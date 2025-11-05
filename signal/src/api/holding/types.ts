export const HOLDING_FLAG_ACTIVE: number = 1
export const HOLDING_FLAG_REMOVED: number = 2
export const HOLDING_FLAG_SOLDOUT: number = 3
export const OPERATION_ACTION_BUY: number = 1
export const OPERATION_ACTION_SELL: number = 2
export const OPERATION_ACTION_INTEREST: number = 3
export const SOLDOUT_FLAG_NO: number = 0
export const SOLDOUT_FLAG_YES: number = 1

export interface CreateRequest {
  type: number
  code: string
}

export type CreateResult = number

export interface ListRequest {
  type?: number
  code?: number
  flag?: number
}

export interface HoldingItem {
  id: number
  type: number
  code: string
  flag: number
  created: Date
  updated: Date
}

export type ListResult = HoldingItem[]

export interface FlagRequest {
  id: number
  flag?: number
}

export type FlagResult = number

export interface RecordRequest {
  id?: number
  type?: number
  code?: string
  flag?: number
}

export interface HoldingRecordItem {
  id: number
  type: number
  code: string
  name: string
  flag: number
  quantity: number
  expense: number
  created: Date
  updated: Date
}

export type RecordResult = HoldingRecordItem[]

export interface OperationListRequest {
  holding?: number
}

export interface HoldingOperationItem {
  id: number
  holding: number
  action: number
  quantity: number
  price: number
  expense: number
  soldout: number
  comment?: string
  created: Date
}

export type OperationListResult = HoldingOperationItem[]

export interface OperationCreateRequest {
  holding: number
  action: number
  quantity: number
  price: number
  expense: number
  comment?: string
  created?: Date
  soldout?: number
}

export type OperationCreateResult = number

///
export interface OperationRemoveRequest {
  id: number
}

export type OperationRemoveResult = number
