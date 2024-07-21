export type InfoModel = {
  id: number
  code: string
  name: string
  type: number
  comment?: string
  updated: Date
}


export type CreateRequest = {
  type: number
  code: string
  comment?: string
}
export type CreateResponse = boolean | undefined

export type InfosRequest = {
  type?: number
  // date?: string
}
export type InfosResponse = InfoModel[]

export type RemoveRequest = {
  id: number
}
export type RemoveResponse = number