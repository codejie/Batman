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

export interface RecordRequest {
  type?: number
  code?: number
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

