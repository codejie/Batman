export interface HistroyRequest {
  type: number
  code: string
  flag?: number // last, all
}

export interface HistroyData {
  price: number
}

export type HistroyResult = HistroyData[]