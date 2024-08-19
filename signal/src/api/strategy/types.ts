export type ArgumentModel = {
  name: string
  type?: string
  unit?: string
  desc?: string
  // value?: any[]
  default?: string | number | boolean
  required: boolean
}

export type ResultFieldModel = {
  name: string
  type?: string
  desc?: string  
}

export type StrategyModel = {
  id: string
  type: number
  name: string
  desc: string
  args?: ArgumentModel[]
  algorithms?: string[]
  result_fields?: ResultFieldModel[]
}

export type TriggerModel = {
    mode: string
    days?: string
    hour?: number
    minute?: number
    seconds?: number
    period: boolean
}

export type ArgumentValuesModel = {
  [key in string]: any
}

export type AlgorithValuesModel = {
  [key in string]: {
    [key in string]: any
  }
}

export type InstanceListItemModel = {
  id: string
  name: string
  strategy: string
  trigger: TriggerModel
  results?: number
  latest_updated?: Date
  run_times: number
  state: number
  is_removed: boolean
}

export type InstanceItemResult = {
  code: string
  name: string
  results: any[]
}
export type InstanceItemModel = {
    id: string
    name: string
    strategy: string
    trigger: TriggerModel
    arg_values?: ArgumentValuesModel
    algo_values?: AlgorithValuesModel
    results?: InstanceItemResult[]
    result_params?: any
    latest_updated?: Date
    run_times: number
    state: number
    is_removed: boolean
}

// Request & Response
export type InfosRequest = {
  type?: number
  id?: string
}

export type InfosResponse = StrategyModel[]

export type ListInstanceRequest = {
    strategy?: string
}

export type ListInstanceResponse = InstanceListItemModel[]

export type GetInstanceRequest = {
  id: string
}

export type GetInstanceResponse = InstanceItemModel

export type RemoveInstanceRequest = {
    id: string
}

export type RemoveInstanceResponse = string

export type CreateInstanceRequest = {
  name: string
  strategy: string
  trigger: TriggerModel
  arg_values?: ArgumentValuesModel
  algo_values?: AlgorithValuesModel
}

export type CreateInstanceResponse = string

export type ResetInstanceRequest = {
  id: string
}

export type ResetInstanceResponse = string
