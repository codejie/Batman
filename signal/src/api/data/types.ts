export const TYPE_INDEX: number = 1
export const TYPE_STOCK: number = 2

export interface HistroyRequest {
  type: number
  code: string
  flag?: number // last, all
}

export interface HistroyData {
  price: number
}

export type HistroyResult = HistroyData[]


// export interface LastHistoryRequest