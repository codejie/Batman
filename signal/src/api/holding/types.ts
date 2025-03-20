export interface CreateRequest {
  type: number
  code: string
}

export interface CreateResponse {
  result: number
}

export interface ListRequest {
  type?: number
  code?: number
  flag?: number
}

export interface UserHoldingRecord {
  id: number
  type: number
  code: string
  quantity: number
  price: number
  expense: number
  comment?: string
  flag: number
  createdAt: string
  updatedAt: string
}

export interface ListResponse {
  result: UserHoldingRecord[]
}

