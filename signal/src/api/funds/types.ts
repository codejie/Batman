const FUNDS_STOCK: number = 1
const OPERATION_ACTION_IN: number = 1
const OPERATION_ACTION_OUT: number = 2

export interface FundsItem {
  id: number,
  type: number,
  amount: number
  updated: Date
}

export interface OperationItem  {
  id: number,
  funds: number,
  action: number,
  amount: number,
  comment?: string,
  created: Date
}

export interface GetRequest {
  type?: number
}

export type GetResult = FundsItem



