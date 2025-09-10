import pandas as pd
import talib

defaultOptions = {
  'timeperiod': 10,
  'column_high': '最高',
  'column_low': '最低',
  'column_close': '收盘',
  'column_volume': '成交量'
}

def title() -> str:
  return "Accumulation/Distribution (A/D) - 聚散指标"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算聚散指标(A/D)。
  Args:
      history_data (pd.DataFrame): 包含历史价格和成交量数据的数据集。
                                   必须包含 '最高', '最低', '收盘', '成交量' 列。
      options (dict): 包含以下键的字典:
                      - 'timeperiod': A/D信号线的移动平均周期 (默认: 10)
                      - 'column_high': 最高价列名 (默认: '最高')
                      - 'column_low': 最低价列名 (默认: '最低')
                      - 'column_close': 收盘价列名 (默认: '收盘')
                      - 'column_volume': 成交量列名 (默认: '成交量')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'AD': A/D值
      - 'AD_Signal': A/D的移动平均信号线
      - 'Signal': 信号 (-1: 卖出, 1: 买入, 0: 中性)
  """
  options = defaultOptions | options
  ad = talib.AD(history_data[options['column_high']],
                history_data[options['column_low']],
                history_data[options['column_close']],
                history_data[options['column_volume']])
  
  ad_signal = ad.rolling(window=options['timeperiod']).mean()

  result = pd.DataFrame({
      'AD': ad,
      'AD_Signal': ad_signal
  })

  # Signal generation: AD crossing its moving average
  result['Signal'] = 0
  # Buy signal: AD crosses above its signal line
  result.loc[(ad > ad_signal) & (ad.shift(1) <= ad_signal.shift(1)), 'Signal'] = 1
  # Sell signal: AD crosses below its signal line
  result.loc[(ad < ad_signal) & (ad.shift(1) >= ad_signal.shift(1)), 'Signal'] = -1

  return result

def report(history_data: pd.DataFrame, ad_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = ad_data[(ad_data['Signal'] == 1) | (ad_data['Signal'] == -1)]

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
