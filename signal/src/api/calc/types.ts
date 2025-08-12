import { symbol } from "vue-types"

export interface AlgorithmItem {
  id: number
  uid: number
  name: string
  remarks: string
  category: number
  type: number
  list_type: number
  data_period: number
  report_period: number
  created: Date
}

export interface StockListItem {
  id: number
  cid: number
  type: number
  code: string
}

export interface ArgumentItem {
  id: number
  cid: number
  category: number
  type: number
  arguments: string
  flag: number
}

// Requests and Results
export interface CreateAlgorithmItemRequest {
  name: string
  category: number
  type: number
  list_type: number
  data_period: number
  report_period: number
  remarks?: string
}
export type CreateAlgorithmItemResult = number

export interface ListAlgorithmItemsRequest {}
export type ListAlgorithmItemsResult = AlgorithmItem[]

export interface DeleteAlgorithmItemRequest {
  id: number
}
export type DeleteAlgorithmItemResult = number

export interface CreateStockListRequest {
  cid: number
  items: StockListItem[]
}
export type CreateStockListResult = number

export interface ListStockListRequest {
  cid: number
}
export type ListStockListResult = StockListItem[]

export interface DeleteStockListRequest {
  cid: number
  id?: number
}
export type DeleteStockListResult = number

export interface CreateArgumentsRequest {
  cid: number
  items: ArgumentItem[]
}
export type CreateArgumentsResult = number

export interface ListArgumentsRequest {
  cid: number
}
export type ListArgumentsResult = ArgumentItem[]

export interface DeleteArgumentsRequest {
  cid: number
  id?: number
}
export type DeleteArgumentsResult = number

export const AlgorithmStockListDefinitions = [
  '持仓', '自选', '持仓&自选', '自定义', '全部'
]

export const AlgorithmDataPeriodDefinitions = [
  '3个月', '6个月', '1年', '2年'
]

export const AlgorithmReportPeriodDefinitions = [
  '当天', '3天', '1周', '1月', '全部'
]

export const AlgorithmCategoryDefinitions = {
  0: {
    name: 'MA',
    title: '均线1',
    description: 'Moving Average (MA) - 移动平均线',
    options: [
      {
        name: 'short_type',
        title: '短期均线类型',
        type: 'string',
        default: 'SMA',
        options: ['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA', 'MAMA', 'T3'],
        description: '',
      },
      {
        name: 'short_period',
        title: '短期均线周期',
        default: 5,
        type: 'number',
        description: '短期均线的计算周期，通常为5或10天'
      },
      {
        name: 'long_type',
        title: '长期均线类型',
        type: 'string',
        default: 'SMA',
        options: ['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA', 'MAMA', 'T3'],
        description: '',
      },
      {
        name: 'long_period',
        title: '长期均线周期',
        default: 20,
        type: 'number',
        description: '长期均线的计算周期，通常为20或30天'
      }      
    ]
  }
}

export const AlgorithmTypeDefinitions = {
  0: {
    category: 0,
    name: 'MA_MA',
    title: '基础移动均线1-0',
    description: 'Moving Average (MA) - 移动平均线'
  },
  1: {
    category: 0,
    name: 'EMA',
    title: '指数移动平均线1-1',
    description: 'Exponential Moving Average (EMA) - 指数移动平均线'
  }
  // Add more algorithm types as needed
}
