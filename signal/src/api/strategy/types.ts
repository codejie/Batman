export type TriggerModel = {
    mode: string
    days?: string
    hour?: number
    minute?: number
    seconds?: number
    period: boolean
}

export type InstanceModel = {
    id: string
    name: string
    strategy: string
    trigger: TriggerModel
    arg_values?: any
    algo_values?: any
    state: number
}


export type ListInstanceRequest = {
    strategy?: string
}

export type ListInstanceResponse = InstanceModel[]

export type RemoveInstanceRequest = {
    id: string
}

export type RemoveInstanceResponse = string