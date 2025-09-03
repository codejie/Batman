
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
  'TrendFollowing': {
    title: '均线趋势',
    description: '均线趋势类算法'
  },
  'MomentumIndicators': {
    title: '动量指标',
    description: '动量指标类算法'
  },
  'VolatilityIndicators': {
    title: '波动率指标',
    description: '波动率指标类算法'
  }
}

export const AlgorithmTypeDefinitions = {
  'TrendFollowing': {
    types: {
      'MA': {
        title: '移动均线',
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
        title: '异同移动平均线',
        description: 'Moving Average Convergence Divergence (MACD) - 平滑异同移动平均线',
        options: [
          {
            name: 'fastperiod',
            title: '快线周期',
            default: 12,
            type: 'number',
            description: '快线(DIF)的计算周期，通常为12天'
          },
          {
            name: 'slowperiod',
            title: '慢线周期',
            default: 26,
            type: 'number',
            description: '慢线(DEA)的计算周期，通常为26天'
          },
          {
            name: 'signalperiod',
            title: '信号线周期',
            default: 9,
            type: 'number',
            description: '信号线(MACD)的计算周期，通常为9天'
          }
        ]
      }
    }
  },
  'MomentumIndicators': {
    types: {
      'RSI': {
        title: '相对强弱指数',
        description: 'Relative Strength Index (RSI) - 相对强弱指数',
        options: [
          {
            name: 'timeperiod',
            title: '周期',
            default: 14,
            type: 'number',
            description: 'RSI的计算周期，通常为14天'
          }
        ]
      }
    }
  },
  'VolatilityIndicators': {
    types: {
      'BOLL': {
        title: '布林带',
        description: 'Bollinger Bands (BOLL) - 布林带',
        options: [
          {
            name: 'timeperiod',
            title: '周期',
            default: 20,
            type: 'number',
            description: '布林带的计算周期，通常为20天'
          },
          {
            name: 'nbdevup',
            title: '上轨标准差倍数',
            default: 2,
            type: 'number',
            description: '布林带上轨的标准差倍数，通常为2'
          },
          {
            name: 'nbdevdn',
            title: '下轨标准差倍数',
            default: 2,
            type: 'number',
            description: '布林带下轨的标准差倍数，通常为2'
          }
        ]
      }
    }
  }
}