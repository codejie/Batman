import pandas as pd
import talib

# MA类型映射表
MA_TYPE_MAP = {
    'SMA': 0,
    'EMA': 1,
    'WMA': 2,
    'DEMA': 3,
    'TEMA': 4,
    'TRIMA': 5,
    'KAMA': 6,
    'MAMA': 7,
    'T3': 8
}

defaultOptions = {
  'fastperiod': 12,
  'fastmatype': 0,   # 0=SMA, 1=EMA, etc.
  'slowperiod': 26,
  'slowmatype': 0,
  'signalperiod': 9,
  'signalmatype': 0,
  'column': '收盘'
}

def title() -> str:
  return "MACDEXT - 扩展型异同移动平均线"

def _resolve_ma_type(val):
    if isinstance(val, str):
        return MA_TYPE_MAP.get(val.upper(), 0)
    return int(val)

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  options = defaultOptions | options

  fastmatype = _resolve_ma_type(options.get('fastmatype', 0))
  slowmatype = _resolve_ma_type(options.get('slowmatype', 0))
  signalmatype = _resolve_ma_type(options.get('signalmatype', 0))

  macd, signal, hist = talib.MACDEXT(
    history_data[options['column']],
    fastperiod=options['fastperiod'],
    fastmatype=fastmatype,
    slowperiod=options['slowperiod'],
    slowmatype=slowmatype,
    signalperiod=options['signalperiod'],
    signalmatype=signalmatype
  )

  result = pd.DataFrame({
    'MACD': macd,
    'Signal_Line': signal,
    'Hist': hist
  })

  result['Signal'] = 0
  # MACD线上穿信号线 - 看涨信号
  result.loc[(result['MACD'] > result['Signal_Line']) & (result['MACD'].shift(1) <= result['Signal_Line'].shift(1)), 'Signal'] = 1
  # MACD线下穿信号线 - 看跌信号
  result.loc[(result['MACD'] < result['Signal_Line']) & (result['MACD'].shift(1) >= result['Signal_Line'].shift(1)), 'Signal'] = -1

  return result

def report(history_data: pd.DataFrame, macd_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = macd_data[(macd_data['Signal'] == 1) | (macd_data['Signal'] == -1)]

  if idx == 0:
    selected_points = signal_points
  elif idx < 0:
    selected_points = signal_points.tail(abs(idx))
  else:
    selected_points = signal_points.iloc[idx-1:]

  for i, row in selected_points.iterrows():
    result.append({
      "index": str(i),
      "price": float(history_data.loc[i, options['column']]),
      "trend": int(row['Signal'])
    })

  return result
