import { DataFrameSetModel } from "@/api/common/types"

export type MACDRequest = {
  value: number[]
  fast?: number
  slow?: number
  period?: number
}

export type MACDResponse = DataFrameSetModel