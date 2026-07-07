import json
from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo
from pandas import DataFrame
import pandas as pd
import requests
from sqlalchemy import delete
from app.database.data import define as Define, utils as Utils
from app.database.data import data_source as DataSource
from app.database import dbEngine
import akshare as ak
from app.logger import logger

def _empty_index_history_df() -> DataFrame:
  return pd.DataFrame(columns=['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额'])

def _index_market_code(symbol: str) -> str:
  code = symbol[-6:]
  market = 'sh' if code.startswith('000') else 'sz'
  return f'{market}{code}'

def _tx_period(period: str) -> str:
  return {
    'daily': 'day',
    'weekly': 'week',
    'monthly': 'month'
  }.get(period, period)

def _format_tx_date(date_str: str) -> str:
  if not date_str:
    return ''
  if '-' in date_str:
    return date_str
  return f'{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}'

def _expand_start_date(start_date: str, period: str) -> str:
  if not start_date:
    return ''
  try:
    delta_days = 90 if period in ('weekly', 'monthly') else 14
    start = datetime.strptime(start_date, '%Y%m%d') - timedelta(days=delta_days)
    return start.strftime('%Y-%m-%d')
  except ValueError:
    return _format_tx_date(start_date)

def _parse_tx_jsonp(text: str) -> dict:
  payload = text.strip()
  if '=' in payload:
    payload = payload.split('=', 1)[1]
  payload = payload.strip().rstrip(';')
  return json.loads(payload)

def _extract_tx_klines(payload, target: str, period_key: str) -> list:
  if isinstance(payload, list):
    return payload
  if not isinstance(payload, dict):
    return []

  data = payload.get('data', {})
  if isinstance(data, list):
    return data
  if not isinstance(data, dict):
    return []

  target_data = data.get(target, {})
  if isinstance(target_data, list):
    return target_data
  if not isinstance(target_data, dict):
    return []

  value = target_data.get(period_key)
  if isinstance(value, list):
    return value
  return []

def _to_float(value, default: float = 0.0) -> float:
  try:
    if value in (None, ''):
      return default
    return float(value)
  except (TypeError, ValueError):
    return default

def _is_today(end_date: str) -> bool:
  if not end_date:
    return False
  try:
    target_date = datetime.strptime(end_date, '%Y-%m-%d').date()
  except ValueError:
    return False

  now = datetime.now(ZoneInfo('Asia/Shanghai'))
  return now.date() == target_date

def _to_tx_amount(fields: list[str]) -> float:
  if len(fields) > 35 and fields[35]:
    parts = fields[35].split('/')
    if len(parts) >= 3:
      return _to_float(parts[2])
  if len(fields) > 57:
    return _to_float(fields[57]) * 10000.0
  if len(fields) > 37:
    return _to_float(fields[37]) * 10000.0
  return 0.0

def _parse_tx_realtime_quote(text: str) -> list[str]:
  payload = text.strip()
  if '=' in payload:
    payload = payload.split('=', 1)[1]
  payload = payload.strip().strip(';').strip('"')
  return payload.split('~') if payload else []

def _append_tx_intraday_realtime_quote(rows: list, symbol: str, target: str, end_date: str, start_date: str, prev_close: float, headers: dict) -> None:
  """
  腾讯指数日 K 可能延迟包含当天数据；当请求今天且日 K 缺当天时，用实时行情补一条当天数据。
  """
  if rows and rows[-1][0] >= end_date:
    return
  if end_date < start_date:
    return
  if prev_close is None or prev_close == 0:
    return

  try:
    response = requests.get(
      'https://qt.gtimg.cn/q={target}'.format(target=target),
      headers=headers,
      proxies={'http': None, 'https': None},
      timeout=8.0
    )
    response.encoding = 'gbk'
    response.raise_for_status()
    fields = _parse_tx_realtime_quote(response.text)
  except Exception as e:
    logger.warning(f"Error downloading TX intraday index history data for {symbol}: {e}")
    return

  if len(fields) <= 35:
    return
  quote_date = fields[30][:8] if len(fields) > 30 else ''
  if quote_date != end_date.replace('-', ''):
    return

  open_price = _to_float(fields[5])
  close_price = _to_float(fields[3])
  high_price = _to_float(fields[33])
  low_price = _to_float(fields[34])
  volume = _to_float(fields[36] if len(fields) > 36 else fields[6])
  amount = _to_tx_amount(fields)
  if close_price == 0:
    return

  change_val = close_price - prev_close
  change_pct = change_val / prev_close * 100
  amplitude = (high_price - low_price) / prev_close * 100

  rows.append([
    end_date,
    open_price,
    close_price,
    high_price,
    low_price,
    volume,
    amount,
    round(amplitude, 2),
    round(change_pct, 2),
    round(change_val, 2)
  ])

def index_zh_a_hist_tx(symbol: str, period: str = "daily", start_date: str = "19700101", end_date: str = "20500101") -> DataFrame:
  """
  腾讯财经 A 股指数历史行情接口，入参与返回列对齐 ak.index_zh_a_hist。
  """
  target = _index_market_code(symbol)
  tx_period = _tx_period(period)
  end = _format_tx_date(end_date)
  count = 640
  url = 'https://web.ifzq.gtimg.cn/appstock/app/kline/kline'
  params = {
    '_var': f'kline_{tx_period}',
    'param': f'{target},{tx_period},,{end},{count}'
  }
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'https://finance.qq.com/'
  }

  try:
    response = requests.get(url, params=params, headers=headers, proxies={'http': None, 'https': None}, timeout=8.0)
    response.raise_for_status()
    payload = _parse_tx_jsonp(response.text)
    klines = _extract_tx_klines(payload, target, tx_period)
    if not klines:
      return _empty_index_history_df()

    start_filter = _format_tx_date(start_date)
    end_filter = _format_tx_date(end_date)
    rows = []
    prev_close = None
    for item in klines:
      if len(item) < 6:
        continue
      date_str = item[0]
      open_price = _to_float(item[1])
      close_price = _to_float(item[2])
      high_price = _to_float(item[3])
      low_price = _to_float(item[4])
      volume = _to_float(item[5])
      amount = _to_float(item[6] if len(item) > 6 else 0.0) * 10000.0

      if prev_close is None or prev_close == 0:
        change_val = 0.0
        change_pct = 0.0
        amplitude = 0.0
      else:
        change_val = close_price - prev_close
        change_pct = change_val / prev_close * 100
        amplitude = (high_price - low_price) / prev_close * 100

      prev_close = close_price
      if date_str < start_filter or date_str > end_filter:
        continue

      rows.append([
        date_str,
        open_price,
        close_price,
        high_price,
        low_price,
        volume,
        amount,
        round(amplitude, 2),
        round(change_pct, 2),
        round(change_val, 2)
      ])

    if tx_period == 'day' and _is_today(end_filter):
      _append_tx_intraday_realtime_quote(rows, symbol, target, end_filter, start_filter, prev_close, headers)

    return pd.DataFrame(rows, columns=_empty_index_history_df().columns)
  except Exception as e:
    logger.warning(f"Error downloading TX index history data for {symbol}: {e}")
    return _empty_index_history_df()

"""
Index
"""
# def download_list() -> None:
#   stmt = delete(Define.InfoTable).where(Define.InfoTable.type == Define.TYPE_INDEX)
#   dbEngine.delete_stmt(stmt)
#   # download
#   index_info = ak.index_stock_info()
#   if not index_info.empty:
#     index_info = index_info.drop(columns=['publish_date'], axis=1)
#     index_info = index_info.rename(columns={
#       'index_code': 'code',
#       'display_name': 'name'
#     })
#     index_info['market'] = index_info['code'].apply(lambda x: 'sh' if x.startswith('000') else 'sz')  
#     index_info['type'] = Define.TYPE_INDEX
#   data = index_info.to_dict(orient='records')
#   dbEngine.bulk_insert_data(Define.InfoTable, data)

def download_list() -> Optional[DataFrame]:
  index_info = ak.index_stock_info()
  if not index_info.empty:
    index_info = index_info.drop(columns=['publish_date'], axis=1)
    index_info = index_info.rename(columns={
      'index_code': 'code',
      'display_name': 'name'
    })
    index_info['market'] = index_info['code'].apply(lambda x: 'sh' if x.startswith('000') else 'sz')  
    index_info['type'] = Define.TYPE_INDEX
    return index_info
  return None

def get_name(code: str) -> Optional[str]:
  return Define.get_name(Define.TYPE_INDEX, code)

def download_history_data(code: str, start: str, end: str, period: str = 'daily') -> Optional[DataFrame]:
  data_source = DataSource.get_market_data_source()
  if data_source == DataSource.DATA_SOURCE_TENCENT:
    data = index_zh_a_hist_tx(symbol=code, period=period, start_date=start, end_date=end)
  else:
    data = ak.index_zh_a_hist(symbol=code, period=period, start_date=start, end_date=end)

  if not data.empty:
    # data = data.drop('股票代码', axis=1)
    data.set_index('日期', inplace=True)
    return data
  else:
    return None
  
def download_spot_data(codes: list[str] = None) -> Optional[DataFrame]:
  # choice of {"沪深重要指数", "上证系列指数", "深证系列指数", "指数成份", "中证系列指数"}
  data = ak.stock_zh_index_spot_em(symbol="沪深重要指数")
  if not data.empty:
    if codes is not None:
      data = data[data['代码'].isin(codes)]
    return data
  return None
