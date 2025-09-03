import pandas as pd
from . import ma, adx, macd, rsi, boll
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
    }
  },
  'MomentumIndicators': {
    'title': '动量指标',
    'types': {
      'RSI': {'calc': rsi.calc, 'report': rsi.report},
    }
  },
  'VolatilityIndicators': {
    'title': '波动率指标',
    'types': {
      'BOLL': {'calc': boll.calc, 'report': boll.report},
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