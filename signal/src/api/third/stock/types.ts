export type DataFrameSetModel = {
  columns: string[],
  data: any[]
}

// Request & Result
export type NewHighRequest = {
  category: number
}
export type NewHighResult = DataFrameSetModel

export type UptrendRequest = {
  days: number
}
export type UptrendResult = DataFrameSetModel

export type HighVolumeRequest = {
  days: number
}
export type HighVolumeResult = DataFrameSetModel

export type RiseVolumePriceRequest = {
  days: number
}
export type RiseVolumePriceResult = DataFrameSetModel

export type LimitUpPoolRequest = {
  date?: string
}
export type LimitUpPoolResult = DataFrameSetModel