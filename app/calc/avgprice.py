import pandas as pd
import talib

defaultOptions = {
  'timeperiod': 10,
  'column_open': '开盘',
  'column_high': '最高',
  'column_low': '最低',
  'column_close': '收盘'
}

def title() -> str:
  return "Average Price (AVGPRICE) - 平均价格"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算平均价格(AVGPRICE)。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含 '开盘', '最高', '最低', '收盘' 列。
      options (dict): 包含以下键的字典:
                      - 'timeperiod': AVGPRICE信号线的移动平均周期 (默认: 10)
                      - 'column_open': 开盘价列名 (默认: '开盘')
                      - 'column_high': 最高价列名 (默认: '最高')
                      - 'column_low': 最低价列名 (默认: '最低')
                      - 'column_close': 收盘价列名 (默认: '收盘')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'AVGPRICE': AVGPRICE值
      - 'AVGPRICE_Signal': AVGPRICE的移动平均信号线
      - 'Signal': 信号 (-1: 卖出, 1: 买入, 0: 中性)
  """
  options = defaultOptions | options
  avgprice = talib.AVGPRICE(history_data[options['column_open']],
                            history_data[options['column_high']],
                            history_data[options['column_low']],
                            history_data[options['column_close']])
  
  avgprice_signal = avgprice.rolling(window=options['timeperiod']).mean()

  result = pd.DataFrame({
      'AVGPRICE': avgprice,
      'AVGPRICE_Signal': avgprice_signal
  })

  # Signal generation: AVGPRICE crossing its moving average
  result['Signal'] = 0
  # Buy signal: AVGPRICE crosses above its signal line
  result.loc[(avgprice > avgprice_signal) & (avgprice.shift(1) <= avgprice_signal.shift(1)), 'Signal'] = 1
  # Sell signal: AVGPRICE crosses below its signal line
  result.loc[(avgprice < avgprice_signal) & (avgprice.shift(1) >= avgprice_signal.shift(1)), 'Signal'] = -1

  return result

def report(history_data: pd.DataFrame, avgprice_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = avgprice_data[(avgprice_data['Signal'] == 1) | (avgprice_data['Signal'] == -1)]

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
