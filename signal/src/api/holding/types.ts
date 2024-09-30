export type CreateRequest = {
  type: number
  code: string
  quantity: number
  expense: number
  comment?: string
  created: string
}
export type CreateResponse = number

export type UpdateRequest = {
  action: number
  type: number
  code: string
  quantity: number
  expense: number
  comment?: string
  created: string
}
export type UpdateResponse = number

export type RemoveRequest = {
  id: number
}
export type RemoveResponse = number

export type RemoveRecordRequest = {
  id: number
}
export type RemoveRecordResponse = number

export type GetHoldingListRequest = {
  type?: number
  code?: string
  with_removed?: boolean
}
export type HoldingModel = {
  id: number
  type: number
  code: string
  name: string
  created: string
  updated: string
  flag: number
}
export type GetHoldingListResponse = HoldingModel[]

export type GetRecordListRequest = {
  holding?: number
  action?: number
  with_removed?: boolean  
}
export type RecordModel = {
  id: number
  holding: number
  action: number
  quantity: number
  expense: number
  comment?: string
  created: string
}
export type GetRecordListResponse = RecordModel[]

export type CalcHoldingListResquest = {
  type?: number
  code?: string
  with_removed?: boolean
}
export type CalcHoldingModel = {
  id: number
  type: number
  code: string
  name: string
  created: string
  updated: string
  flag: number
  quantity: number
  expense: number
}
export type CalcHoldingListResponse = CalcHoldingModel[]

export type GetHoldingRecordRequest = {
  type?: number
  code?: string
  action?: number
  with_removed?: boolean
}
export type HoldingRecordModel = {
  id: number
  holding: number
  type: number
  code: string
  name: string
  action: number
  quantity: number
  expense: number
  created: string
  updated: string // record's create
  flag: number
}
export type GetHoldingRecordResponse = HoldingRecordModel[]
