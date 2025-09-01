
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
  'MA': {
    title: '均线',
    description: 'Moving Average (MA) - 移动平均线',
    options: [
      {
        name: 'short_type',
        title: '短期均线类型',
        type: 'option',
        default: 'SMA',
        options: ['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA', 'MAMA', 'T3'],
        description: "['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA', 'MAMA', 'T3']"
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
        type: 'option',
        default: 'SMA',
        options: ['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA', 'MAMA', 'T3'],
        description: "['SMA', 'EMA', 'WMA', 'DEMA', 'TEMA', 'TRIMA', 'KAMA', 'MAMA', 'T3']"
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
  'ADX': {
    title: '平均趋向指数',
    description: 'Average Directional Index (ADX) - 平均趋向指标',
    options: [
      {
        name: 'period',
        title: '周期',
        default: 14,
        type: 'number',
        description: 'ADX指标的计算周期，通常为14天'
      },
      {
        name: 'threshold',
        title: '阈值',
        default: 25,
        type: 'number',
        description: '用于判断趋势强弱的阈值，通常设为25'
      }
    ]
  },
  'MACD': {
    title: 'MACD',
    description: 'Moving Average Convergence Divergence (MACD) - 平滑异同移动平均线',
    options: [
    ]
  }
}

export const AlgorithmTypeDefinitions = {
  'MA': {
    'MA_MA': {
      title: '基础移动均线',
      description: 'Moving Average (MA) - 移动平均线'
    },
    'EMA': {
      title: '指数移动平均线',
      description: 'Exponential Moving Average (EMA) - 指数移动平均线'
    }
  },
  'ADX': {
    'ADX': {
      title: '平均趋向指数',
      description: 'Average Directional Index (ADX) - 平均趋向指标'
    }
  }
}




// export type AlgorithmTypeOptionType = {
//   key: string,
//   options: {
//     [key in string]: any
//   }
// }