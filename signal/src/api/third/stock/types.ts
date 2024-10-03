// export type DataFrameSetModel = {
//   columns: string[],
//   data: any[]
// }

import { DataFrameSetModel } from "@/api/common/types"

// Request & Response
export type NewHighRequest = {
  category: number
}
export type NewHighResponse = DataFrameSetModel

export type UptrendRequest = {
  days: number
}
export type UptrendResponse = DataFrameSetModel

export type HighVolumeRequest = {
  days: number
}
export type HighVolumeResponse = DataFrameSetModel

export type RiseVolumePriceRequest = {
  days: number
}
export type RiseVolumePriceResponse = DataFrameSetModel

export type LimitUpPoolRequest = {
  date?: string
}
export type LimitUpPoolResponse = DataFrameSetModel