const FUNDS_STOCK: number = 1
// const OPERATION_ACTION_IN: number = 1
// const OPERATION_ACTION_OUT: number = 2

export interface FundsItem {
  id: number,
  type: number,
  amount: number // 资金，本金
  available: number // 可用资金
  updated: Date
}

export interface OperationItem  {
  id: number,
  funds: number,
  // action: number,
  amount: number,
  comment?: string,
  created: Date
}

// export interface CreateRequest {
//   type?: number
//   amount: number
// }
// export type CreateResult = number

export interface GetRequest {
  type?: number
}
export type GetResult = FundsItem

export interface UpdateRequest {
  // id: number,
  type: number
  amount: number
}
export type UpdateResult = number

