import pandas as pd
import talib
from typing import Optional

defaultOptions = {
  'timeperiod': 20,
  'nbdevup': 2,
  'nbdevdn': 2,
  'column': '收盘'
}

def title() -> str:
  return "Bollinger Bands (BOLL) - 布林带"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算布林带(BOLL)。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含一个名为 '收盘' 的列。
      options (dict): 包含以下键的字典:
                      - 'timeperiod': 计算布林带的周期 (默认: 20)
                      - 'nbdevup': 上轨标准差倍数 (默认: 2)
                      - 'nbdevdn': 下轨标准差倍数 (默认: 2)
                      - 'column': 用于计算布林带的列名 (默认: '收盘')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'UpperBand': 布林带上轨
      - 'MiddleBand': 布林带中轨
      - 'LowerBand': 布林带下轨
      - 'Signal': 信号 (-1: 卖出信号, 0: 中性, 1: 买入信号)
  """
  options = defaultOptions | options
  upperband, middleband, lowerband = talib.BBANDS(
      history_data[options['column']],
      timeperiod=options['timeperiod'],
      nbdevup=options['nbdevup'],
      nbdevdn=options['nbdevdn']
  )

  result = pd.DataFrame({
      'UpperBand': upperband,
      'MiddleBand': middleband,
      'LowerBand': lowerband
  })

  result['Signal'] = 0
  # Buy signal: Price crosses below lower band
  result.loc[history_data[options['column']] < lowerband, 'Signal'] = 1
  # Sell signal: Price crosses above upper band
  result.loc[history_data[options['column']] > upperband, 'Signal'] = -1

  return result

def report(history_data: pd.DataFrame, boll_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = boll_data[(boll_data['Signal'] == 1) | (boll_data['Signal'] == -1)]

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
