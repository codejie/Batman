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

export type LinkInfoModel = {
  title: string,
  url: string,
  tip?: string,
  needCode?: boolean,
  inWindow?: boolean
}

export type GroupInfoModel = {
  title: string,
  icon: string,
  links: LinkInfoModel[]
}

export type InfoLinksRequest = {
  flag?: number
}
export type InfoLinksResult =  GroupInfoModel[]