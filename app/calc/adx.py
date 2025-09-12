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

  result['Signal'] = 0
  is_trending = result['ADX'] > options['threshold']
  
  # Buy Signal
  is_di_buy_cross = (result['+DI'] > result['-DI']) & (result['+DI'].shift(1) <= result['-DI'].shift(1))
  result.loc[is_trending & is_di_buy_cross, 'Signal'] = 1

  # Sell Signal
  is_di_sell_cross = (result['+DI'] < result['-DI']) & (result['+DI'].shift(1) >= result['-DI'].shift(1))
  result.loc[is_trending & is_di_sell_cross, 'Signal'] = -1

  return result

def report(history_data: pd.DataFrame, adx_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options
  
  result: list[dict] = []
  
  signal_points = adx_data[adx_data['Signal'] != 0]

  if idx == 0:
      selected_points = signal_points
  elif idx < 0:
      selected_points = signal_points.tail(abs(idx))
  else: # idx > 0
      selected_points = signal_points.iloc[idx-1:]

  for i, row in selected_points.iterrows():
      result.append({
          "index": str(i),
          "price": float(history_data.loc[i, options['columns'][2]]),
          "trend": int(row['Signal'])
      })
        
  return result

# ADX, OBV, RSI