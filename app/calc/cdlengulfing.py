import pandas as pd
import talib

defaultOptions = {
  'column_open': '开盘',
  'column_high': '最高',
  'column_low': '最低',
  'column_close': '收盘'
}

def title() -> str:
  return "Engulfing Pattern (CDLENGULFING) - 吞噬模式"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项识别吞噬模式。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含 '开盘', '最高', '最低', '收盘' 列。
      options (dict): 包含以下键的字典:
                      - 'column_open': 开盘价列名 (默认: '开盘')
                      - 'column_high': 最高价列名 (默认: '最高')
                      - 'column_low': 最低价列名 (默认: '最低')
                      - 'column_close': 收盘价列名 (默认: '收盘')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'CDLENGULFING': 100 (看涨), -100 (看跌), 0 (未识别)
      - 'Signal': 信号 (1: 看涨, -1: 看跌, 0: 中性)
  """
  options = defaultOptions | options
  cdlengulfing = talib.CDLENGULFING(history_data[options['column_open']],
                                  history_data[options['column_high']],
                                  history_data[options['column_low']],
                                  history_data[options['column_close']])

  result = pd.DataFrame({
      'CDLENGULFING': cdlengulfing
  })

  result['Signal'] = 0
  result.loc[cdlengulfing == 100, 'Signal'] = 1  # Bullish pattern
  result.loc[cdlengulfing == -100, 'Signal'] = -1 # Bearish pattern

  return result

def report(history_data: pd.DataFrame, pattern_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = pattern_data[(pattern_data['Signal'] == 1) | (pattern_data['Signal'] == -1)]

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
