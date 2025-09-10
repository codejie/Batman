import pandas as pd
import talib

defaultOptions = {
  'acceleration': 0.02,
  'maximum': 0.2,
  'column_high': '最高',
  'column_low': '最低'
}

def title() -> str:
  return "Parabolic SAR - 抛物线转向指标"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算抛物线转向指标(SAR)。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含 '最高' 和 '最低' 列。
      options (dict): 包含以下键的字典:
                      - 'acceleration': 加速因子 (默认: 0.02)
                      - 'maximum': 加速因子最大值 (默认: 0.2)
                      - 'column_high': 用于计算的最高价列名 (默认: '最高')
                      - 'column_low': 用于计算的最低价列名 (默认: '最低')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'SAR': SAR值
      - 'Signal': 信号 (-1: 卖出, 1: 买入, 0: 中性)
  """
  options = defaultOptions | options
  sar = talib.SAR(history_data[options['column_high']], history_data[options['column_low']], acceleration=options['acceleration'], maximum=options['maximum'])

  result = pd.DataFrame({
      'SAR': sar
  })

  # Signal generation: Price crossing SAR
  result['Signal'] = 0
  # Buy signal: SAR flips below the low price
  result.loc[(sar < history_data[options['column_low']]) & (sar.shift(1) > history_data[options['column_high']].shift(1)), 'Signal'] = 1
  # Sell signal: SAR flips above the high price
  result.loc[(sar > history_data[options['column_high']]) & (sar.shift(1) < history_data[options['column_low']].shift(1)), 'Signal'] = -1

  return result

def report(history_data: pd.DataFrame, sar_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = sar_data[(sar_data['Signal'] == 1) | (sar_data['Signal'] == -1)]

  if idx == 0:
      selected_points = signal_points
  elif idx < 0:
      selected_points = signal_points.tail(abs(idx))
  else: # idx > 0
      selected_points = signal_points.iloc[idx-1:]

  for i, row in selected_points.iterrows():
      result.append({
          "index": str(i),
          "price": float(history_data.loc[i, '收盘']), # Use close price for reporting
          "trend": int(row['Signal'])
      })

  return result
