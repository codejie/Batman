export const HOLDING_FLAG_ACTIVE: number = 1;
export const HOLDING_FLAG_REMOVED: number = 2;
export const OPERATION_ACTION_BUY: number = 1;
export const OPERATION_ACTION_SELL: number = 2;

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

export interface HoldingData {
  id: number
  type: number
  code: string
  flag: number
  created: Date
  updated: Date
}

export type ListResult = HoldingData[]

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

export interface HoldingRecord {
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

export type RecordResult = HoldingRecord[]

export interface OperationListRequest {
  holding?: number
}

export interface HoldingOperationData {
  id: number
  holding: number
  action: number
  quantity: number
  price: number
  expense: number
  comment?: string
  created: Date
}

export type OperationListResult = HoldingOperationData[]

export interface OperationCreateRequest {
  holding: number
  action: number
  quantity: number
  price: number
  expense: number
  comment?: string
}

export type OperationCreateResult = number

///
export interface OperationRemoveRequest {
  id: number
}

export type OperationRemoveResult = number