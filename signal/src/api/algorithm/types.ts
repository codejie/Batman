export type ArgumentModel = {
  name: string
  type?: string
  unit?: string
  desc?: string
  default?: any
  required: boolean
}

export type DataModel = {
  name: string
  type: string
  desc?: string  
}

export type ResultModel = {
  name: string
  type: string
  desc?: string  
}

export type AlgorithmModel = {
  name: string
  desc: string
  args?: ArgumentModel[]
  data?: DataModel[]
  results?: ResultModel[]
}

// Request & Response
export type InfosRequest = {
  name?: string
}

export type InfosResponse = AlgorithmModel[] | AlgorithmModel
