
export const AlgorithmStockListDefinitions = [
  '持仓列表', '自选列表', '自定义列表', '全部列表', '持仓&自选'
]

export const AlgorithmDataPeriodDefinitions = [
  '三个月', '六个月', '一年', '两年'
]

export const AlgorithmReportPeriodDefinitions = [
  '当天', '最近三天', '最近一周', '最近一月', '全部'
]

export type AlgorithmCategoryOptionType = {
  name: string,
  title: string,
  type: string,
  default: any,
  options?: any,
  description: string
}

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
        description: ''
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
        description: ''
      },
      {
        name: 'long_period',
        title: '长期均线周期',
        default: 20,
        type: 'number',
        description: '长期均线的计算周期，通常为20或30天'
      }      
    ]
  },
  1: {
    name: 'MACD',
    title: 'MACD1',
    description: 'Moving Average Convergence Divergence (MACD) - 平滑异同移动平均线',
    options: [
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


export type AlgorithmTypeOptionType = {
  key: string,
  options: {
    [key in string]: any
  }
}