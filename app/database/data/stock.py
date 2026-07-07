"""
Stock
"""
import json
from datetime import datetime, time, timedelta
from typing import Optional
from zoneinfo import ZoneInfo
from pandas import DataFrame
import pandas as pd
import akshare as ak
import requests
from sqlalchemy import delete
from app.database import dbEngine
from app.database.data import define as Define
from app.database.data import data_source as DataSource
from app.database.data import utils as Utils

from app.logger import logger

def _empty_stock_history_df() -> DataFrame:
  return pd.DataFrame(columns=['日期', '股票代码', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'])

def _stock_market_code(symbol: str) -> str:
  code = symbol[-6:]
  if code.startswith(('60', '68', '90')):
    return f'sh{code}'
  return f'sz{code}'

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

def _extract_tx_klines(payload, target: str, data_key: str, period_key: str) -> list:
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

  for key in (data_key, period_key):
    value = target_data.get(key)
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

def _is_before_a_share_close(end_date: str) -> bool:
  if not end_date:
    return False
  try:
    target_date = datetime.strptime(end_date, '%Y-%m-%d').date()
  except ValueError:
    return False

  now = datetime.now(ZoneInfo('Asia/Shanghai'))
  return now.date() == target_date and now.time() < time(15, 0)

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
  腾讯复权日 K 在盘中通常不包含当天数据；闭市前用实时行情补一条非复权盘中数据。
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
    logger.warning(f"Error downloading TX intraday stock history data for {symbol}: {e}")
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
    symbol[-6:],
    open_price,
    close_price,
    high_price,
    low_price,
    volume,
    amount,
    round(amplitude, 2),
    round(change_pct, 2),
    round(change_val, 2),
    0.0
  ])

def stock_zh_a_hist_tx(symbol: str, period: str = "daily", start_date: str = "19700101", end_date: str = "20500101", adjust: str = "") -> DataFrame:
  """
  腾讯财经 A 股历史行情接口，入参与返回列对齐 ak.stock_zh_a_hist。
  """
  target = _stock_market_code(symbol)
  tx_period = _tx_period(period)
  adjust = adjust or ''
  end = _format_tx_date(end_date)
  count = 640

  if adjust in ('qfq', 'hfq'):
    url = 'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get'
    data_key = f'{adjust}{tx_period}'
    params = {
      '_var': f'kline_{tx_period}{adjust}',
      'param': f'{target},{tx_period},,{end},{count},{adjust}'
    }
  else:
    url = 'https://web.ifzq.gtimg.cn/appstock/app/kline/kline'
    data_key = tx_period
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
    klines = _extract_tx_klines(payload, target, data_key, tx_period)
    if not klines:
      return _empty_stock_history_df()

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
        symbol[-6:],
        open_price,
        close_price,
        high_price,
        low_price,
        volume,
        amount,
        round(amplitude, 2),
        round(change_pct, 2),
        round(change_val, 2),
        0.0
      ])

    if adjust in ('qfq', 'hfq') and tx_period == 'day' and _is_before_a_share_close(end_filter):
      _append_tx_intraday_realtime_quote(rows, symbol, target, end_filter, start_filter, prev_close, headers)

    return pd.DataFrame(rows, columns=_empty_stock_history_df().columns)
  except Exception as e:
    logger.warning(f"Error downloading TX stock history data for {symbol}: {e}")
    return _empty_stock_history_df()

# def download_list() -> None:
#   # delete
#   stmt = delete(Define.InfoTable).where(Define.InfoTable.type == Define.TYPE_STOCK)
#   dbEngine.delete_stmt(stmt)
#   # download
#   stock_info = ak.stock_info_a_code_name()
#   stock_info['type'] = Define.TYPE_STOCK
#   stock_info['market'] = None
#   data = stock_info.to_dict(orient='records')
#   dbEngine.bulk_insert_data(Define.InfoTable, data)

def download_list() -> Optional[DataFrame]:
  # delete
  # stmt = delete(Define.InfoTable).where(Define.InfoTable.type == Define.TYPE_STOCK)
  # dbEngine.delete_stmt(stmt)
  # download
  stock_info = ak.stock_info_a_code_name()
  if not stock_info.empty:
    stock_info['type'] = Define.TYPE_STOCK
    stock_info['market'] = None

    return stock_info
  return None

def get_name(code: str) -> Optional[str]:
  return Define.get_name(Define.TYPE_STOCK, code)

def download_history_data(code: str, start: str, end: str, period: str = 'daily', adjust: str = 'qfq') -> Optional[DataFrame]:
  data_source = DataSource.get_market_data_source()
  if data_source == DataSource.DATA_SOURCE_TENCENT:
    data = stock_zh_a_hist_tx(symbol=code, period=period, adjust=adjust, start_date=start, end_date=end)
  else:
    data = ak.stock_zh_a_hist(symbol=code, period=period, adjust=adjust, start_date=start, end_date=end)

  if not data.empty:
    data = data.drop('股票代码', axis=1)
    data.set_index('日期', inplace=True)
    return data
  else:
    return None

# def fetch_history_data(code: str, start: str, end: str, period: str = 'daily', adjust: str = 'qfq') -> list[Define.HistoryData]:
#   return Define.fetch_history_data(Define.TYPE_STOCK, code, start, end, period, adjust)

def download_spot_data(codes: list[str] = None) -> Optional[DataFrame]:
  try:
    data = ak.stock_zh_a_spot_em()
    if not data.empty:
      # data = data.drop('序号')
      # data.set_index('代码', inplace=True)
      data = data.rename(columns={
        '市盈率-动态': '市盈率',
        '5分钟涨跌': '涨跌5分钟',
        '60日涨跌幅': '涨跌幅60日'
      })
      if codes is not None:
        data = data[data['代码'].isin(codes)]
      return data
  except Exception as e:
    logger.warning(f"Error downloading spot data: {e}")
  return None

################################################
"""
Stock Info
"""
def download_info(code: str) -> Optional[DataFrame]:
  try:
    data = ak.stock_individual_info_em(symbol=code)
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading stock info for {code}: {e}")
  return None

"""
财务指标数据
"""
def download_financial_abstract_indicator(code: str, indicator: str = '按报告期') -> Optional[DataFrame]:
  """
    indicator:  choice of {"按报告期", "按年度", "按单季度"}
  """
  try:
    data = ak.stock_financial_abstract_ths(symbol=code, indicator=indicator)
    if not data.empty:
      # data = data.set_index('报告日期')
      return data
  except Exception as e:
    logger.warning(f"Error downloading financial indicator {indicator} for {code}: {e}")
  return None

"""
财务分析指标数据
"""
def download_financial_analysis_indicator(code: str, start: str = "2020") -> Optional[DataFrame]:
  try:
    data = ak.stock_financial_analysis_indicator(symbol=code, start_year=start)
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading financial analysis for {code}: {e}")
  return None

"""
现金流数据(报告期)
"""
def download_cash_report_data(code: str) -> Optional[DataFrame]:
  try:
    data = ak.stock_cash_flow_sheet_by_report_em(symbol=code)
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading cash report data for {code}: {e}")
  return None

"""
估值指标
"""
def download_valuation_indicator(code: str) -> Optional[DataFrame]:
  try:
    data = ak.stock_a_indicator_lg(symbol=code)
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading valuation indicator for {code}: {e}")
  return None

"""
业绩报表
"""
# def download_performance_report(date: str) -> Optional[DataFrame]:
#   try:
#     data = ak.stock_yjbb_em(date=date)# .stock_yjbb_em(symbol=code)
#     if not data.empty:
#       return data
#   except Exception as e:
#     logger.warning(f"Error downloading performance report for {code}: {e}")
#   return None

"""
分红配股
"""
# def download_dividend_distribution(code: str) -> Optional[DataFrame]:
#   try:
#     data = ak.stock_fhpg_em(symbol=code)
#     if not data.empty:
#       return data
#   except Exception as e:
#     logger.warning(f"Error downloading dividend distribution for {code}: {e}")
#   return None

"""
行业数据
"""
def _download_industry_data() -> Optional[DataFrame]:
  try:
    data = ak.stock_board_industry_name_em()
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading industry data : {e}")
  return None

"""
行业排名
"""
# def download_industry_rank(symbol: str = '行业排名') -> Optional[DataFrame]:
#   try:
#     data = ak.stock_rank_em(symbol=symbol)
#     if not data.empty:
#       return data
#   except Exception as e:
#     logger.warning(f"Error downloading industry rank for {symbol}: {e}")
#   return None

"""
公司新闻
"""
# def download_company_news(code: str) -> Optional[DataFrame]:
#   try:
#     data = ak.stock_news_em(symbol=code)
#     if not data.empty:
#       return data
#   except Exception as e:
#     logger.warning(f"Error downloading company news for {code}: {e}")
#   return None

"""
公司公告
"""
# def download_company_announcements(code: str) -> Optional[DataFrame]:
#   try:
#     data = ak.stock_zh_a_alerts_cls(symbol=code)
#     if not data.empty:
#       return data
#   except Exception as e:
#     logger.warning(f"Error downloading company announcements for {code}: {e}")
#   return None

"""
个股研报
"""
def download_research_report(code: str) -> Optional[DataFrame]:
  try:
    data = ak.stock_research_report_em(symbol=code)
    if not data.empty:
      return data
  except Exception as e:
    logger.warning(f"Error downloading research report for {code}: {e}")
  return None
