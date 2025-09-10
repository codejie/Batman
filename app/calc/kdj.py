import pandas as pd
import talib

defaultOptions = {
  'fastk_period': 9,
  'slowk_period': 3,
  'slowd_period': 3,
  'column_high': '最高',
  'column_low': '最低',
  'column_close': '收盘'
}

def title() -> str:
  return "Stochastic Oscillator (KDJ) - 随机指标"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算随机指标(KDJ)。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含 '最高', '最低', '收盘' 列。
      options (dict): 包含以下键的字典:
                      - 'fastk_period': 快速K线周期 (默认: 9)
                      - 'slowk_period': 慢速K线周期 (默认: 3)
                      - 'slowd_period': 慢速D线周期 (默认: 3)
                      - 'column_high': 最高价列名 (默认: '最高')
                      - 'column_low': 最低价列名 (默认: '最低')
                      - 'column_close': 收盘价列名 (默认: '收盘')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'K': K值
      - 'D': D值
      - 'J': J值
      - 'Signal': 信号 (-1: 卖出, 1: 买入, 0: 中性)
  """
  options = defaultOptions | options
  
  # Calculate %K and %D
  slowk, slowd = talib.STOCH(
      history_data[options['column_high']],
      history_data[options['column_low']],
      history_data[options['column_close']],
      fastk_period=options['fastk_period'],
      slowk_period=options['slowk_period'],
      slowk_matype=0, # SMA
      slowd_period=options['slowd_period'],
      slowd_matype=0  # SMA
  )

  # Calculate %J: J = 3 * D - 2 * K (or 3 * K - 2 * D, depending on definition)
  # Common definition: J = 3 * D - 2 * K
  j = 3 * slowd - 2 * slowk

  result = pd.DataFrame({
      'K': slowk,
      'D': slowd,
      'J': j
  })

  # Signal generation: K/D crossover and overbought/oversold levels
  result['Signal'] = 0
  # Buy signal: K crosses above D and both are below 20 (oversold)
  result.loc[(slowk > slowd) & (slowk.shift(1) <= slowd.shift(1)) & (slowk < 20), 'Signal'] = 1
  # Sell signal: K crosses below D and both are above 80 (overbought)
  result.loc[(slowk < slowd) & (slowk.shift(1) >= slowd.shift(1)) & (slowk > 80), 'Signal'] = -1

  return result

def report(history_data: pd.DataFrame, kdj_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = kdj_data[(kdj_data['Signal'] == 1) | (kdj_data['Signal'] == -1)]

  if idx == 0:
      selected_points = signal_points
  elif idx < 0:
      selected_points = signal_points.tail(abs(idx))
  else: # idx > 0
      selected_points = signal_points.iloc[idx-1:]

  for i, row in selected_points.iterrows():
      result.append({
          "index": str(i),
          "price": float(history_data.loc[i, options['column_close']]),
          "trend": int(row['Signal'])
      })

  return result
