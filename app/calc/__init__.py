import pandas as pd
from . import ma, adx, macd, macdext, rsi, boll, mom, obv, sar, kdj, ad, atr, natr, avgprice, medprice, cdlhammer, cdlengulfing, cdlmorningstar, cdldoji, cdleveningstar, cdl3whitesoldiers, cdl3blackcrows, cdldarkcloudcover, ht_dcperiod, ht_dcphase, vwap
from typing import Callable, Tuple, Optional

def list_to_df(data: list) -> Optional[pd.DataFrame]:
  if data:
    ret = pd.DataFrame([item.dict() for item in data])
    if not ret.empty:
      ret.set_index('日期', inplace=True)
      return ret
  return None

# 分类和命名调整为 ta-lib 官方定义
CALC_MODULES = {
  'OverlapStudies': {  # 覆盖研究
    'title': 'Overlap Studies',
    'types': {
      'MA': {'calc': ma.calc, 'report': ma.report},
      'SAR': {'calc': sar.calc, 'report': sar.report},
    }
  },
  'MomentumIndicators': {  # 动量指标
    'title': 'Momentum Indicators',
    'types': {
      'ADX': {'calc': adx.calc, 'report': adx.report},
      'MACD': {'calc': macd.calc, 'report': macd.report},
      'MACDEXT': {'calc': macdext.calc, 'report': macdext.report},
      'RSI': {'calc': rsi.calc, 'report': rsi.report},
      'MOM': {'calc': mom.calc, 'report': mom.report},
      'KDJ': {'calc': kdj.calc, 'report': kdj.report},
    }
  },
  'VolatilityIndicators': {  # 波动率指标
    'title': 'Volatility Indicators',
    'types': {
      'BOLL': {'calc': boll.calc, 'report': boll.report},
      'ATR': {'calc': atr.calc, 'report': atr.report},
      'NATR': {'calc': natr.calc, 'report': natr.report},
    }
  },
  'VolumeIndicators': {  # 成交量指标
    'title': 'Volume Indicators',
    'types': {
      'OBV': {'calc': obv.calc, 'report': obv.report},
      'AD': {'calc': ad.calc, 'report': ad.report},
      'VWAP': {'calc': vwap.calc, 'report': vwap.report},
    }
  },
  'PriceTransform': {  # 价格变换
    'title': 'Price Transform',
    'types': {
      'AVGPRICE': {'calc': avgprice.calc, 'report': avgprice.report},
      'MEDPRICE': {'calc': medprice.calc, 'report': medprice.report},
    }
  },
  'PatternRecognition': {  # K线形态识别
    'title': 'Pattern Recognition',
    'types': {
      'CDLHAMMER': {'calc': cdlhammer.calc, 'report': cdlhammer.report},
      'CDLENGULFING': {'calc': cdlengulfing.calc, 'report': cdlengulfing.report},
      'CDLMORNINGSTAR': {'calc': cdlmorningstar.calc, 'report': cdlmorningstar.report},
      'CDLDOJI': {'calc': cdldoji.calc, 'report': cdldoji.report},
      'CDLEVENINGSTAR': {'calc': cdleveningstar.calc, 'report': cdleveningstar.report},
      'CDL3WHITESOLDIERS': {'calc': cdl3whitesoldiers.calc, 'report': cdl3whitesoldiers.report},
      'CDL3BLACKCROWS': {'calc': cdl3blackcrows.calc, 'report': cdl3blackcrows.report},
      'CDLDARKCLOUDCOVER': {'calc': cdldarkcloudcover.calc, 'report': cdldarkcloudcover.report},
    }
  },
  'CycleIndicators': {  # 周期指标
    'title': 'Cycle Indicators',
    'types': {
      'HT_DCPERIOD': {'calc': ht_dcperiod.calc, 'report': ht_dcperiod.report},
      'HT_DCPHASE': {'calc': ht_dcphase.calc, 'report': ht_dcphase.report},
    }
  }
}

def get_calc_functions(category: str, type: str) -> Tuple[Optional[Callable], Optional[Callable]]:
  """
  A factory function that returns calculation and report functions based on category and type.

  Args:
    category (str): The category of the calculation (e.g., 'OverlapStudies' for MA, SAR).
    type (str): The type of calculation within the category (e.g., 'MA', 'ADX').

  Returns:
    Tuple[Optional[Callable], Optional[Callable]]: A tuple containing the calc function
                                                   and the report function, or (None, None) if not found.
  """
  category_definitions = CALC_MODULES.get(category)
  if category_definitions:
    type_definition = category_definitions.get('types').get(type)
    if type_definition:
      return (type_definition.get('calc'), type_definition.get('report'))
  
  return (None, None)