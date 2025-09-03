import pandas as pd
import talib

defaultOptions = {
  'fastperiod': 12,
  'slowperiod': 26,
  'signalperiod': 9,
  'column': '收盘'
}

def title() -> str:
  return "MACD - 异同移动平均线"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算异同移动平均线(MACD)。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含一个名为 '收盘' 的列。
      options (dict): 包含以下键的字典:
                      - 'fastperiod': 快速EMA周期 (默认: 12)
                      - 'slowperiod': 慢速EMA周期 (默认: 26)
                      - 'signalperiod': 信号线EMA周期 (默认: 9)
                      - 'column': 用于计算MACD的列名 (默认: '收盘')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'MACD': MACD线
      - 'Signal_Line': 信号线
      - 'Hist': MACD柱
      - 'Signal': 趋势信号 (-1: 看跌, 0: 中性, 1: 看涨)
  """
  options = defaultOptions | options
  macd, signal, hist = talib.MACD(history_data[options['column']], 
                                  fastperiod=options['fastperiod'], 
                                  slowperiod=options['slowperiod'], 
                                  signalperiod=options['signalperiod'])

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
      # 返回所有信号点
      selected_points = signal_points
  elif idx < 0:
      # 返回最近的idx个信号点
      selected_points = signal_points.tail(abs(idx))
  else: # idx > 0
      # 返回从第idx个信号点开始的所有点
      selected_points = signal_points.iloc[idx-1:]

  for i, row in selected_points.iterrows():
      result.append({
          "index": str(i),
          "price": float(history_data.loc[i, options['column']]),
          "trend": int(row['Signal'])
      })
        
  return result
