import pandas as pd
import talib

defaultOptions = {
  'timeperiod': 14,
  'column_high': '最高',
  'column_low': '最低',
  'column_close': '收盘'
}

def title() -> str:
  return "Average True Range (ATR) - 平均真实波幅"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算平均真实波幅(ATR)。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含 '最高', '最低', '收盘' 列。
      options (dict): 包含以下键的字典:
                      - 'timeperiod': ATR的计算周期 (默认: 14)
                      - 'column_high': 最高价列名 (默认: '最高')
                      - 'column_low': 最低价列名 (默认: '最低')
                      - 'column_close': 收盘价列名 (默认: '收盘')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'ATR': ATR值
      - 'Signal': 信号 (1: 高波动, -1: 低波动, 0: 中性)
  """
  options = defaultOptions | options
  atr = talib.ATR(history_data[options['column_high']],
                  history_data[options['column_low']],
                  history_data[options['column_close']],
                  timeperiod=options['timeperiod'])

  result = pd.DataFrame({
      'ATR': atr
  })

  # Signal generation: Simple threshold for volatility
  # This is a simplified signal for demonstration. ATR is typically used to confirm trends or set stop-losses.
  result['Signal'] = 0
  # Example: If ATR is significantly higher than its recent average, indicate high volatility
  # For a more robust signal, one might compare ATR to a moving average of ATR or a fixed threshold.
  # Here, we'll just use a simple relative threshold for illustration.
  mean_atr = atr.rolling(window=options['timeperiod']).mean()
  result.loc[atr > mean_atr * 1.2, 'Signal'] = 1  # High volatility
  result.loc[atr < mean_atr * 0.8, 'Signal'] = -1 # Low volatility

  return result

def report(history_data: pd.DataFrame, atr_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = atr_data[(atr_data['Signal'] == 1) | (atr_data['Signal'] == -1)]

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
