import pandas as pd
import talib

defaultOptions = {
  'column_close': '收盘'
}

def title() -> str:
  return "Hilbert Transform - Dominant Cycle Phase (HT_DCPHASE) - 希尔伯特变换-主导周期相位"

def calc(history_data: pd.DataFrame, options: dict = defaultOptions) -> pd.DataFrame:
  """
  根据提供的历史数据和选项计算希尔伯特变换-主导周期相位。
  Args:
      history_data (pd.DataFrame): 包含历史价格数据的数据集。
                                   必须包含 '收盘' 列。
      options (dict): 包含以下键的字典:
                      - 'column_close': 收盘价列名 (默认: '收盘')
  Returns:
      pd.DataFrame: 包含以下列的DataFrame:
      - 'HT_DCPHASE': 主导周期相位值
      - 'Signal': 信号 (1: 相位上升, -1: 相位下降, 0: 中性)
  """
  options = defaultOptions | options
  ht_dcphase = talib.HT_DCPHASE(history_data[options['column_close']])

  result = pd.DataFrame({
      'HT_DCPHASE': ht_dcphase
  })

  # Signal generation: Simple trend of the phase
  result['Signal'] = 0
  result.loc[ht_dcphase > ht_dcphase.shift(1), 'Signal'] = 1  # Phase increasing
  result.loc[ht_dcphase < ht_dcphase.shift(1), 'Signal'] = -1 # Phase decreasing

  return result

def report(history_data: pd.DataFrame, dcphase_data: pd.DataFrame, idx: int = 0, options: dict = defaultOptions) -> list[dict]:
  options = defaultOptions | options

  result: list[dict] = []

  signal_points = dcphase_data[(dcphase_data['Signal'] == 1) | (dcphase_data['Signal'] == -1)]

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
