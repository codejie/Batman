import pandas as pd
import talib
from typing import Optional

defaultOptions = {
  'short_type': 'SMA',
  'short_period': 5,
  'long_type': 'SMA',
  'long_period': 20,
  'column': '收盘'
}

ma_type_map = {
    'SMA': 0,
    'EMA': 1,
    'WMA': 2,
    'DEMA': 3,
    'TEMA': 4,
    'TRIMA': 5,
    'KAMA': 6,
    'MAMA': 7,
    'T3': 8
}

def title() -> str:
  return "Moving Average (MA) - 移动平均线"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算移动平均线(MA)及其趋势。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含一个名为 '收盘' 的列。
      options (dict): 包含以下键的字典:
                      - 'short_type': 短期MA类型 (默认: 'SMA')
                      - 'short_period': 短期MA周期 (默认: 5)
                      - 'long_type': 长期MA类型 (默认: 'SMA')
                      - 'long_period': 长期MA周期 (默认: 20)
                      - 'column': 用于计算MA的列名 (默认: '收盘')
      Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'Short': 短期MA
      - 'Long': 长期MA
      - 'Signal': 趋势信号 (-1: 下跌, 0: 中性, 1: 上涨)
  """
  short = talib.MA(history_data[options['column']], timeperiod=options['short_period'], matype=ma_type_map[options['short_type']])
  long = talib.MA(history_data[options['column']], timeperiod=options['long_period'], matype=ma_type_map[options['long_type']])

  result = pd.DataFrame({
      'Short': short,
      'Long': long
  })

  for i in range(1, len(result['Short'])):
    if result['Short'].iloc[i] > result['Long'].iloc[i] and result['Short'].iloc[i-1] <= result['Long'].iloc[i-1]:
      result.loc[result.index[i], 'Signal'] = 1 # Uptrend
    elif result['Short'].iloc[i] < result['Long'].iloc[i] and result['Short'].iloc[i-1] >= result['Long'].iloc[i-1]:
      result.loc[result.index[i], 'Signal'] = -1  # Downtrend
    else:
      result.loc[result.index[i], 'Signal'] = 0 # Neutral

  return result

def report(history_data: pd.DataFrame, ma_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[str]:  
  result = []
  if idx == 0:
    for i in range(len(ma_data)):
      if ma_data['Signal'].iloc[i] == 1 or ma_data['Signal'].iloc[i] == -1:
        trend = "Uptrend" if ma_data['Signal'].iloc[i] == 1 else "Downtrend"
        result.append(f"{ma_data.index[i]}: {trend} [Price: {history_data[options['column']].iloc[i]}]")
  elif idx < 0:
    for i in range(len(ma_data) + idx, len(ma_data)):
      if ma_data['Signal'].iloc[i] == 1 or ma_data['Signal'].iloc[i] == -1:
        trend = "Uptrend" if ma_data['Signal'].iloc[i] == 1 else "Downtrend"
        result.append(f"{ma_data.index[i]}: {trend} [Price: {history_data[options['column']].iloc[i]}]")
  elif idx > 0:
    for i in range(idx, len(ma_data)):
      if ma_data['Signal'].iloc[i] == 1 or ma_data['Signal'].iloc[i] == -1:
        trend = "Uptrend" if ma_data['Signal'].iloc[i] == 1 else "Downtrend"
        result.append(f"{ma_data.index[i]}: {trend} [Price: {history_data[options['column']].iloc[i]}]")

  return result