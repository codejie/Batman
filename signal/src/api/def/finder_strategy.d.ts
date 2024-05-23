// Strategy
export interface IArgumentInfo {
    name: string,
    type: string,
    unit: string,
    desc: string,
    default: string
}

export interface IAlgorithmInfo {
    name: string,
    desc: string,
    args: IArgumentInfo[]
}

export interface IStrategyInfo {
    name: string,
    desc: string,
    algorithm: IAlgorithmInfo,
}

// Instance
export interface IITriggerInfo {
    mode: string,
    hour?: number,
    minute?: number
}

export interface IInstanceInfo {
    id: string,
    title: string,
    trigger: IITriggerInfo,
    strategy: string,
    args: any,
    runTimes: number,
    lastUpdated: string,
    duration:string,
    result: {
        items: any[] 
        
    }   
}