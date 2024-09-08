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