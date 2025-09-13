export const AlgorithmStockListDefinitions = [
  '持仓列表',
  '自选列表',
  '自定义列表',
  '全部列表',
  '持仓&自选'
]

export const AlgorithmDataPeriodDefinitions = ['三个月', '六个月', '一年', '两年']

export const AlgorithmReportPeriodDefinitions = ['当天', '最近三天', '最近一周', '最近一月', '全部']

export type AlgorithmCategoryOptionType = {
  name: string
  title: string
  type: string
  default: any
  options?: any
  description: string
}

export const AlgorithmCategoryDefinitions = {
  TrendFollowing: {
    title: '均线趋势',
    description: '均线趋势类算法'
  },
  MomentumIndicators: {
    title: '动量指标',
    description: '动量指标类算法'
  },
  VolatilityIndicators: {
    title: '波动率指标',
    description: '波动率指标类算法'
  },
  VolumeIndicators: {
    title: '成交量指标',
    description: '成交量指标类算法'
  },
  PriceTransformation: {
    title: '价格变换',
    description: '价格变换类算法'
  },
  CandlestickPatterns: {
    title: 'K线形态识别',
    description: 'K线形态识别类算法'
  },
  CycleIndicators: {
    title: '周期指标',
    description: '周期指标类算法'
  }
}

export const AlgorithmTypeDefinitions = {
  TrendFollowing: {
    types: {
      MA: {
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
      ADX: {
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
      MACD: {
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
      },
      SAR: {
        title: '抛物线转向指标',
        description: 'Parabolic SAR - 抛物线转向指标',
        options: [
          {
            name: 'acceleration',
            title: '加速因子',
            default: 0.02,
            type: 'number',
            description: '加速因子，通常为0.02'
          },
          {
            name: 'maximum',
            title: '加速因子最大值',
            default: 0.2,
            type: 'number',
            description: '加速因子的最大值，通常为0.2'
          }
        ]
      }
    }
  },
  MomentumIndicators: {
    types: {
      RSI: {
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
      },
      MOM: {
        title: '动量指标',
        description: 'Momentum (MOM) - 动量指标',
        options: [
          {
            name: 'timeperiod',
            title: '周期',
            default: 10,
            type: 'number',
            description: 'MOM的计算周期，通常为10天'
          }
        ]
      },
      KDJ: {
        title: '随机指标',
        description: 'Stochastic Oscillator (KDJ) - 随机指标',
        options: [
          {
            name: 'fastk_period',
            title: '快速K线周期',
            default: 9,
            type: 'number',
            description: '快速K线(Fast %K)的计算周期，通常为9天'
          },
          {
            name: 'slowk_period',
            title: '慢速K线周期',
            default: 3,
            type: 'number',
            description: '慢速K线(%K)的平滑周期，通常为3天'
          },
          {
            name: 'slowd_period',
            title: '慢速D线周期',
            default: 3,
            type: 'number',
            description: '慢速D线(%D)的平滑周期，通常为3天'
          }
        ]
      }
    }
  },
  VolatilityIndicators: {
    types: {
      BOLL: {
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
      },
      ATR: {
        title: '平均真实波幅',
        description: 'Average True Range (ATR) - 平均真实波幅',
        options: [
          {
            name: 'timeperiod',
            title: '周期',
            default: 14,
            type: 'number',
            description: 'ATR的计算周期，通常为14天'
          }
        ]
      },
      NATR: {
        title: '归一化平均真实波幅',
        description: 'Normalized Average True Range (NATR) - 归一化平均真实波幅',
        options: [
          {
            name: 'timeperiod',
            title: '周期',
            default: 14,
            type: 'number',
            description: 'NATR的计算周期，通常为14天'
          }
        ]
      }
    }
  },
  VolumeIndicators: {
    types: {
      OBV: {
        title: '能量潮',
        description: 'On-Balance Volume (OBV) - 能量潮',
        options: [
          {
            name: 'timeperiod',
            title: '信号线周期',
            default: 10,
            type: 'number',
            description: 'OBV信号线的移动平均计算周期，通常为10天'
          }
        ]
      },
      AD: {
        title: '聚散指标',
        description: 'Accumulation/Distribution (A/D) - 聚散指标',
        options: [
          {
            name: 'timeperiod',
            title: '信号线周期',
            default: 10,
            type: 'number',
            description: 'A/D信号线的移动平均计算周期，通常为10天'
          }
        ]
      }
    }
  },
  PriceTransformation: {
    types: {
      AVGPRICE: {
        title: '平均价格',
        description: 'Average Price (AVGPRICE) - 平均价格',
        options: [
          {
            name: 'timeperiod',
            title: '信号线周期',
            default: 10,
            type: 'number',
            description: 'AVGPRICE信号线的移动平均计算周期，通常为10天'
          }
        ]
      },
      MEDPRICE: {
        title: '中位数价格',
        description: 'Median Price (MEDPRICE) - 中位数价格',
        options: [
          {
            name: 'timeperiod',
            title: '信号线周期',
            default: 10,
            type: 'number',
            description: 'MEDPRICE信号线的移动平均计算周期，通常为10天'
          }
        ]
      }
    }
  },
  CandlestickPatterns: {
    types: {
      CDLHAMMER: {
        title: '锤头线',
        description: 'Hammer (CDLHAMMER) - 锤头线',
        options: []
      },
      CDLENGULFING: {
        title: '吞噬模式',
        description: 'Engulfing Pattern (CDLENGULFING) - 吞噬模式',
        options: []
      },
      CDLMORNINGSTAR: {
        title: '晨星',
        description: 'Morning Star (CDLMORNINGSTAR) - 晨星',
        options: []
      },
      CDLDOJI: {
        title: '十字星',
        description: 'Doji (CDLDOJI) - 十字星',
        options: []
      },
      CDLEVENINGSTAR: {
        title: '黄昏星',
        description: 'Evening Star (CDLEVENINGSTAR) - 黄昏星',
        options: []
      },
      CDL3WHITESOLDIERS: {
        title: '三白兵',
        description: 'Three White Soldiers (CDL3WHITESOLDIERS) - 三白兵',
        options: []
      },
      CDL3BLACKCROWS: {
        title: '三只乌鸦',
        description: 'Three Black Crows (CDL3BLACKCROWS) - 三只乌鸦',
        options: []
      },
      CDLDARKCLOUDCOVER: {
        title: '乌云盖顶',
        description: 'Dark Cloud Cover (CDLDARKCLOUDCOVER) - 乌云盖顶',
        options: []
      }
    }
  },
  CycleIndicators: {
    types: {
      HT_DCPERIOD: {
        title: '希尔伯特变换-主导周期',
        description:
          'Hilbert Transform - Dominant Cycle Period (HT_DCPERIOD) - 希尔伯特变换-主导周期',
        options: []
      },
      HT_DCPHASE: {
        title: '希尔伯特变换-主导周期相位',
        description:
          'Hilbert Transform - Dominant Cycle Phase (HT_DCPHASE) - 希尔伯特变换-主导周期相位',
        options: []
      }
    }
  }
}
