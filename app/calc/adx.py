from typing import Optional
import pandas as pd
import talib

defaultOptions = {
  'period': 14,
  'divider': 25,
  'signal': True,
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
  adx = talib.ADX(history_data[options['columns'][0]], history_data[options['columns'][1]], history_data[options['columns'][2]], timeperiod=options['period'])
  plus_di = talib.PLUS_DI(history_data[options['columns'][0]], history_data[options['columns'][1]], history_data[options['columns'][2]], timeperiod=options['period'])
  minus_di = talib.MINUS_DI(history_data[options['columns'][0]], history_data[options['columns'][1]], history_data[options['columns'][2]], timeperiod=options['period'])

  result = pd.DataFrame({
      'ADX': adx,
      '+DI': plus_di,
      '-DI': minus_di
  })

  if options['signal']:
    for i in range(1, len(result)):
      if result['ADX'].iloc[i] > options['divider']:
        if  result['+DI'].iloc[i-1] <= result['-DI'].iloc[i-1] and result['+DI'].iloc[i] > result['-DI'].iloc[i]:
          result.loc[result.index[i], 'Signal'] = 1
        elif result['+DI'].iloc[i-1] >= result['-DI'].iloc[i-1] and result['+DI'].iloc[i] < result['-DI'].iloc[i]:
          result.loc[result.index[i], 'Signal'] = -1
        else:
          result.loc[result.index[i], 'Signal'] = 0
      else:
        result.loc[result.index[i], 'Signal'] = 0

  return result

def report(history_data: pd.DataFrame, adx_data: pd.DataFrame, idx: Optional[int] = None, options: dict = defaultOptions) -> list[str]:
  result = []
  if idx is None:
    for i in range(len(adx_data)):
      if adx_data['Signal'].iloc[i] == 1 or adx_data['Signal'].iloc[i] == -1:
        result.append(f"{adx_data.index[i]}: {'Uptrend' if adx_data['Signal'].iloc[i] == 1 else 'Downtrend'} [ADX: {adx_data['ADX'].iloc[i]} / Price: {history_data['收盘'].iloc[i]}]")
  elif idx < 0:
    for i in range(len(adx_data) + idx, len(adx_data)):
      if adx_data['Signal'].iloc[i] == 1 or adx_data['Signal'].iloc[i] == -1:
        result.append(f"{adx_data.index[i]}: {'Uptrend' if adx_data['Signal'].iloc[i] == 1 else 'Downtrend'} [ADX: {adx_data['ADX'].iloc[i]} /Price: {history_data['收盘'].iloc[i]}]")
  elif idx > 0:
    for i in range(idx, len(adx_data)):
      if adx_data['Signal'].iloc[i] == 1 or adx_data['Signal'].iloc[i] == -1:
        result.append(f"{adx_data.index[i]}: {'Uptrend' if adx_data['Signal'].iloc[i] == 1 else 'Downtrend'} [ADX: {adx_data['ADX'].iloc[i]} /Price: {history_data['收盘'].iloc[i]}]")

  return result

# ADX, OBV, RSI