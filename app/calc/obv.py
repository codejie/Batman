import pandas as pd
import talib

defaultOptions = {
  'timeperiod': 10,
  'column_close': '收盘',
  'column_volume': '成交量'
}

def title() -> str:
  return "On-Balance Volume (OBV) - 能量潮"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算能量潮(OBV)。
  Args:
      history_data (pd.DataFrame): 包含历史价格和成交量数据的数据集。
                                   必须包含 '收盘' 和 '成交量' 列。
      options (dict): 包含以下键的字典:
                      - 'timeperiod': OBV信号线的移动平均周期 (默认: 10)
                      - 'column_close': 用于计算的收盘价列名 (默认: '收盘')
                      - 'column_volume': 用于计算的成交量列名 (默认: '成交量')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'OBV': OBV值
      - 'OBV_Signal': OBV的移动平均信号线
      - 'Signal': 信号 (-1: 卖出, 1: 买入, 0: 中性)
  """
  options = defaultOptions | options
  obv = talib.OBV(history_data[options['column_close']], history_data[options['column_volume']])
  
  obv_signal = obv.rolling(window=options['timeperiod']).mean()

  result = pd.DataFrame({
      'OBV': obv,
      'OBV_Signal': obv_signal
  })

  # Signal generation: OBV crossing its moving average
  result['Signal'] = 0
  # Buy signal: OBV crosses above its signal line
  result.loc[(obv > obv_signal) & (obv.shift(1) <= obv_signal.shift(1)), 'Signal'] = 1
  # Sell signal: OBV crosses below its signal line
  result.loc[(obv < obv_signal) & (obv.shift(1) >= obv_signal.shift(1)), 'Signal'] = -1

  return result

def report(history_data: pd.DataFrame, obv_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = obv_data[(obv_data['Signal'] == 1) | (obv_data['Signal'] == -1)]

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
