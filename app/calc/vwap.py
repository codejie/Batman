import pandas as pd

defaultOptions = {
  'timeperiod': 30,
  'column_high': '最高',
  'column_low': '最低',
  'column_close': '收盘',
  'column_volume': '成交量'
}

def title() -> str:
  return "Volume Weighted Average Price (VWAP) - 成交量加权平均价"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算VWAP。
  Args:
      history_data (pd.DataFrame): 包含历史价格和成交量数据的数据集。
                                   必须包含 '最高', '最低', '收盘', '成交量' 列。
      options (dict): 包含以下键的字典:
                      - 'timeperiod': VWAP的计算周期 (默认: 30)
                      - 'column_high': 最高价列名 (默认: '最高')
                      - 'column_low': 最低价列名 (默认: '最低')
                      - 'column_close': 收盘价列名 (默认: '收盘')
                      - 'column_volume': 成交量列名 (默认: '成交量')
  Returns:
      pd.DataFrame: 包含 'VWAP' 列的DataFrame。
  """
  options = defaultOptions | options
  
  tp = (history_data[options['column_high']] + history_data[options['column_low']] + history_data[options['column_close']]) / 3
  tpv = tp * history_data[options['column_volume']]
  
  rolling_tpv = tpv.rolling(window=options['timeperiod']).sum()
  rolling_volume = history_data[options['column_volume']].rolling(window=options['timeperiod']).sum()
  
  vwap = rolling_tpv / rolling_volume

  result = pd.DataFrame({
      'VWAP': vwap
  })

  close_price = history_data[options['column_close']]
  result['Price'] = close_price
  result['Signal'] = 0
  # Buy signal: close price crosses above VWAP
  result.loc[(close_price > vwap) & (close_price.shift(1) <= vwap.shift(1)), 'Signal'] = 1
  # Sell signal: close price crosses below VWAP
  result.loc[(close_price < vwap) & (close_price.shift(1) >= vwap.shift(1)), 'Signal'] = -1

  return result

def report(history_data: pd.DataFrame, vwap_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options
  
  result: list[dict] = []
  
  signal_points = vwap_data[vwap_data['Signal'] != 0]

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
