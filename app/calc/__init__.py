import pandas as pd
from . import ma, adx
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
  'MA': {
    'MA_MA': ma,
    'EMA': ma,
  },
  'ADX': {
    'ADX': adx,
  },
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
  category_modules = CALC_MODULES.get(category)
  if category_modules:
    module = category_modules.get(type)
    if module:
      return (getattr(module, 'calc', None), getattr(module, 'report', None))
  
  return (None, None)