import pandas as pd
import talib

defaultOptions = {
  'timeperiod': 10,
  'column_high': '最高',
  'column_low': '最低',
  'column_close': '收盘' # For reporting price
}

def title() -> str:
  return "Median Price (MEDPRICE) - 中位数价格"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算中位数价格(MEDPRICE)。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含 '最高' 和 '最低' 列。
      options (dict): 包含以下键的字典:
                      - 'timeperiod': MEDPRICE信号线的移动平均周期 (默认: 10)
                      - 'column_high': 最高价列名 (默认: '最高')
                      - 'column_low': 最低价列名 (默认: '最低')
                      - 'column_close': 收盘价列名 (默认: '收盘')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'MEDPRICE': MEDPRICE值
      - 'MEDPRICE_Signal': MEDPRICE的移动平均信号线
      - 'Signal': 信号 (-1: 卖出, 1: 买入, 0: 中性)
  """
  options = defaultOptions | options
  medprice = talib.MEDPRICE(history_data[options['column_high']],
                            history_data[options['column_low']])
  
  medprice_signal = medprice.rolling(window=options['timeperiod']).mean()

  result = pd.DataFrame({
      'MEDPRICE': medprice,
      'MEDPRICE_Signal': medprice_signal
  })

  # Signal generation: MEDPRICE crossing its moving average
  result['Signal'] = 0
  # Buy signal: MEDPRICE crosses above its signal line
  result.loc[(medprice > medprice_signal) & (medprice.shift(1) <= medprice_signal.shift(1)), 'Signal'] = 1
  # Sell signal: MEDPRICE crosses below its signal line
  result.loc[(medprice < medprice_signal) & (medprice.shift(1) >= medprice_signal.shift(1)), 'Signal'] = -1

  return result

def report(history_data: pd.DataFrame, medprice_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = medprice_data[(medprice_data['Signal'] == 1) | (medprice_data['Signal'] == -1)]

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
