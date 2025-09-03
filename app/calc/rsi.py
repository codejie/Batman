import pandas as pd
import talib
from typing import Optional

defaultOptions = {
  'timeperiod': 14,
  'column': '收盘'
}

def title() -> str:
  return "Relative Strength Index (RSI) - 相对强弱指数"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算相对强弱指数(RSI)。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含一个名为 '收盘' 的列。
      options (dict): 包含以下键的字典:
                      - 'timeperiod': 计算RSI的周期 (默认: 14)
                      - 'column': 用于计算RSI的列名 (默认: '收盘')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'RSI': RSI值
      - 'Signal': 信号 (-1: 卖出信号, 0: 中性, 1: 买入信号)
  """
  options = defaultOptions | options
  rsi = talib.RSI(history_data[options['column']], timeperiod=options['timeperiod'])

  result = pd.DataFrame({
      'RSI': rsi
  })

  # Generate signals based on common RSI thresholds
  # RSI > 70: Overbought (sell signal)
  # RSI < 30: Oversold (buy signal)
  result['Signal'] = 0
  result.loc[rsi > 70, 'Signal'] = -1 # Sell signal
  result.loc[rsi < 30, 'Signal'] = 1  # Buy signal

  return result

def report(history_data: pd.DataFrame, rsi_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = rsi_data[(rsi_data['Signal'] == 1) | (rsi_data['Signal'] == -1)]

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
