export interface HistroyRequest {
  type: number
  code: string
  flag?: number // last, all
}

export interface HistroyData {}

export type HistroyResult = HistroyData[]