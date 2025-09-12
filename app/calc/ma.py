# from dataclasses import dataclass
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

# @dataclass
# class ReportType:
#   index: str
#   price: float
#   trend: int  # -1: downtrend, 0: neutral, 1: up

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
  options = defaultOptions | options
  short = talib.MA(history_data[options['column']], timeperiod=options['short_period'], matype=ma_type_map[options['short_type']])
  long = talib.MA(history_data[options['column']], timeperiod=options['long_period'], matype=ma_type_map[options['long_type']])

  result = pd.DataFrame({
      'Short': short,
      'Long': long
  })

  result['Signal'] = 0
  # Golden cross
  result.loc[(result['Short'] > result['Long']) & (result['Short'].shift(1) <= result['Long'].shift(1)), 'Signal'] = 1
  # Death cross
  result.loc[(result['Short'] < result['Long']) & (result['Short'].shift(1) >= result['Long'].shift(1)), 'Signal'] = -1

  return result

def report(history_data: pd.DataFrame, ma_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options
  
  result: list[dict] = []
  
  signal_points = ma_data[ma_data['Signal'] != 0]

  if idx == 0:
      selected_points = signal_points
  elif idx < 0:
      selected_points = signal_points.tail(abs(idx))
  else: # idx > 0
      selected_points = signal_points.iloc[idx-1:]

  for i, row in selected_points.iterrows():
      result.append({
          "index": str(i),
          "price": float(history_data.loc[i, options['column']]),
          "trend": int(row['Signal'])
      })
        
  return result