export interface IStrategyData {
  id: number
  name: string
  description: string
  arguments?: IStrategyArgumentData[]
}

export interface IStrategyArgumentData {
  name: string
  unit: string
  value?: number
  notes: string
}

export interface IStrategyInstanceData {
  id?: number
  strategyId?: number
  title: string
  trigger: any,
  lastRunTime?: string
  runTimes?: number
  scheduleTime?: string
  arguments?: IStrategyArgumentData[]
}

export interface IRoleData {
  key: string
  name: string
  description: string
  routes: any
}

export interface ITransactionData {
  orderId: string
  timestamp: string | number
  username: string
  price: number
  status: string
}

export interface IUserData {
  id: number
  username: string
  password: string
  name: string
  email: string
  phone: string
  avatar: string
  introduction: string
  roles: string[]
}
