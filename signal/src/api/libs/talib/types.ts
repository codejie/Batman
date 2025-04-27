import { DataFrameSetModel } from "@/api/third/stock/types"

export type MACDRequest = {
  value: number[]
  fast?: number
  slow?: number
  period?: number
}

export type MACDResult = DataFrameSetModel