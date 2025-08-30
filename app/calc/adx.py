from typing import Optional
import pandas as pd
import talib

defaultOptions = {
  'period': 14,
  'threshold': 25,
  # 'signal': True,
  'columns': ['最高', '最低', '收盘']
}

def title() -> str:
    return "Average Directional Index (ADX) - 平均趋向指数"

"""
### Result: DataFrame
- ADX: 0 - 100
- +DI
- -DI
- Signal: -1: downtrend, 0: neutral, 1: uptrend
"""

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  options = defaultOptions | options

  adx = talib.ADX(history_data[options['columns'][0]], history_data[options['columns'][1]], history_data[options['columns'][2]], timeperiod=options['period'])
  plus_di = talib.PLUS_DI(history_data[options['columns'][0]], history_data[options['columns'][1]], history_data[options['columns'][2]], timeperiod=options['period'])
  minus_di = talib.MINUS_DI(history_data[options['columns'][0]], history_data[options['columns'][1]], history_data[options['columns'][2]], timeperiod=options['period'])

  result = pd.DataFrame({
      'ADX': adx,
      '+DI': plus_di,
      '-DI': minus_di
  })

  # if options['signal']:
  for i in range(1, len(result)):
    if result['ADX'].iloc[i] > options['threshold']:
      if  result['+DI'].iloc[i-1] <= result['-DI'].iloc[i-1] and result['+DI'].iloc[i] > result['-DI'].iloc[i]:
        result.loc[result.index[i], 'Signal'] = 1
      elif result['+DI'].iloc[i-1] >= result['-DI'].iloc[i-1] and result['+DI'].iloc[i] < result['-DI'].iloc[i]:
        result.loc[result.index[i], 'Signal'] = -1
      else:
        result.loc[result.index[i], 'Signal'] = 0
    else:
      result.loc[result.index[i], 'Signal'] = 0

  return result

def report(history_data: pd.DataFrame, adx_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options
  
  result: list[dict] = []
  
  start_index = 0
  if idx > 0:
    start_index = idx
  elif idx < 0:
    start_index = len(adx_data) + idx

  for i in range(start_index, len(adx_data)):
    signal = adx_data['Signal'].iloc[i]
    if signal == 1 or signal == -1:
      result.append({
        "index": str(adx_data.index[i]),
        "price": float(history_data[options['columns'][2]].iloc[i]),
        "trend": signal
      })
      
  return result

# ADX, OBV, RSI