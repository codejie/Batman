import pandas as pd
from . import ma, adx, macd, rsi, boll, mom, obv, sar, kdj, ad, atr, natr, avgprice, medprice, cdlhammer, cdlengulfing, cdlmorningstar, cdldoji, cdleveningstar, cdl3whitesoldiers, cdl3blackcrows, cdldarkcloudcover, ht_dcperiod, ht_dcphase
from typing import Callable, Tuple, Optional


def list_to_df(data: list) -> Optional[pd.DataFrame]:
  if data:
    ret = pd.DataFrame([item.dict() for item in data])
    if not ret.empty:
      ret.set_index('日期', inplace=True)
      return ret
  return None

# Define a mapping from (category, type) to the corresponding module
# Category 0: Technical Indicators
CALC_MODULES = {
  'TrendFollowing': {
    'title': '均线趋势',
    'types': {
      'MA': {'calc': ma.calc, 'report': ma.report},
      'ADX': {'calc': adx.calc, 'report': adx.report},
      'MACD': {'calc': macd.calc, 'report': macd.report},
      'SAR': {'calc': sar.calc, 'report': sar.report},
    }
  },
  'MomentumIndicators': {
    'title': '动量指标',
    'types': {
      'RSI': {'calc': rsi.calc, 'report': rsi.report},
      'MOM': {'calc': mom.calc, 'report': mom.report},
      'KDJ': {'calc': kdj.calc, 'report': kdj.report},
    }
  },
  'VolatilityIndicators': {
    'title': '波动率指标',
    'types': {
      'BOLL': {'calc': boll.calc, 'report': boll.report},
      'ATR': {'calc': atr.calc, 'report': atr.report},
      'NATR': {'calc': natr.calc, 'report': natr.report},
    }
  },
  'VolumeIndicators': {
    'title': '成交量指标',
    'types': {
      'OBV': {'calc': obv.calc, 'report': obv.report},
      'AD': {'calc': ad.calc, 'report': ad.report},
    }
  },
  'PriceTransformation': {
    'title': '价格变换',
    'types': {
      'AVGPRICE': {'calc': avgprice.calc, 'report': avgprice.report},
      'MEDPRICE': {'calc': medprice.calc, 'report': medprice.report},
    }
  },
  'CandlestickPatterns': {
    'title': 'K线形态识别',
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
  'CycleIndicators': {
    'title': '周期指标',
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
    category (str): The category of the calculation (e.g., 'MA' for Technical Indicators).
    type (str): The type of calculation within the category (e.g., 'MA_MA' for MA, 'ADX_ADX' for ADX).

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