import pandas as pd
import talib
from typing import Optional

defaultOptions = {
  'timeperiod': 10,
  'column': '收盘'
}

def title() -> str:
  return "Momentum (MOM) - 动量指标"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算动量指标(MOM)。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含一个名为 '收盘' 的列。
      options (dict): 包含以下键的字典:
                      - 'timeperiod': 计算MOM的周期 (默认: 10)
                      - 'column': 用于计算MOM的列名 (默认: '收盘')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'MOM': MOM值
      - 'Signal': 信号 (-1: 卖出信号, 0: 中性, 1: 买入信号)
  """
  options = defaultOptions | options
  mom = talib.MOM(history_data[options['column']], timeperiod=options['timeperiod'])

  result = pd.DataFrame({
      'MOM': mom
  })

  # Generate signals based on MOM crossing zero
  # MOM > 0: Upward momentum (buy signal)
  # MOM < 0: Downward momentum (sell signal)
  result['Signal'] = 0
  result.loc[mom > 0, 'Signal'] = 1  # Buy signal
  result.loc[mom < 0, 'Signal'] = -1 # Sell signal

  return result

def report(history_data: pd.DataFrame, mom_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = mom_data[(mom_data['Signal'] == 1) | (mom_data['Signal'] == -1)]

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
