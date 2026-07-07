"""
Fund
"""
from functools import lru_cache
from typing import Optional

import akshare as ak
import pandas as pd
import requests
from pandas import DataFrame
from sqlalchemy import select

from app.database import dbEngine
from app.database.data import define as Define
from app.logger import logger

HISTORY_COLUMNS = ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']
SPOT_COLUMNS = ['序号', '代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', '最高', '最低', '今开', '昨收', '量比', '换手率', '市盈率', '市净率', '总市值', '流通市值', '涨速', '涨跌5分钟', '涨跌幅60日', '年初至今涨跌幅']
ETF_CODE_PREFIXES = ('159', '510', '511', '512', '513', '515', '516', '517', '518', '560', '561', '562', '563', '588', '589')
LOF_CODE_PREFIXES = ('160', '161', '162', '163', '164', '165', '166', '167', '168', '169', '501', '502')

def _empty_history_df() -> DataFrame:
  return pd.DataFrame(columns=HISTORY_COLUMNS)

def _empty_spot_df() -> DataFrame:
  return pd.DataFrame(columns=SPOT_COLUMNS)

def _to_float(value, default: float = 0.0) -> float:
  try:
    if value in (None, ''):
      return default
    return float(value)
  except (TypeError, ValueError):
    return default

def _normalize_code(code) -> str:
  return str(code).strip().zfill(6)

def _fund_market_code(code: str) -> str:
  code = _normalize_code(code)
  return f"sh{code}" if code.startswith('5') else f"sz{code}"

def _first_existing_column(data: DataFrame, columns: list[str]) -> Optional[str]:
  for column in columns:
    if column in data.columns:
      return column
  return None

def _rename_first_existing(data: DataFrame, target: str, candidates: list[str]) -> DataFrame:
  if target in data.columns:
    return data
  source = _first_existing_column(data, candidates)
  if source:
    return data.rename(columns={source: target})
  return data

def _normalize_numeric_columns(data: DataFrame, columns: list[str]) -> DataFrame:
  for column in columns:
    if column in data.columns:
      data[column] = pd.to_numeric(data[column], errors='coerce').fillna(0.0)
  return data

def _parse_tx_realtime_quote(text: str) -> list[str]:
  payload = text.strip()
  if '=' in payload:
    payload = payload.split('=', 1)[1]
  payload = payload.strip().strip(';').strip('"')
  return payload.split('~') if payload else []

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

def _tx_spot_row(code: str, seq: int = 1) -> Optional[dict]:
  target = _fund_market_code(code)
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'https://finance.qq.com/'
  }
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
    logger.warning(f"Error downloading TX fund spot data for {code}: {e}")
    return None

  if len(fields) <= 35:
    return None

  latest = _to_float(fields[3])
  prev_close = _to_float(fields[4])
  open_price = _to_float(fields[5])
  high_price = _to_float(fields[33])
  low_price = _to_float(fields[34])
  volume = _to_float(fields[36] if len(fields) > 36 else fields[6])
  if latest == 0:
    return None

  change_value = latest - prev_close if prev_close else _to_float(fields[31] if len(fields) > 31 else 0.0)
  change_rate = change_value / prev_close * 100 if prev_close else _to_float(fields[32] if len(fields) > 32 else 0.0)
  amplitude = (high_price - low_price) / prev_close * 100 if prev_close else 0.0

  return {
    '序号': seq,
    '代码': _normalize_code(code),
    '名称': fields[1] if len(fields) > 1 else _normalize_code(code),
    '最新价': latest,
    '涨跌幅': round(change_rate, 2),
    '涨跌额': round(change_value, 3),
    '成交量': volume,
    '成交额': _to_tx_amount(fields),
    '振幅': round(amplitude, 2),
    '最高': high_price,
    '最低': low_price,
    '今开': open_price,
    '昨收': prev_close,
    '量比': None,
    '换手率': None,
    '市盈率': None,
    '市净率': None,
    '总市值': None,
    '流通市值': None,
    '涨速': None,
    '涨跌5分钟': None,
    '涨跌幅60日': None,
    '年初至今涨跌幅': None
  }

def _fund_market_from_db(code: str) -> Optional[int]:
  try:
    stmt = select(Define.InfoTable.market).where(Define.InfoTable.type == Define.TYPE_FUND).where(Define.InfoTable.code == _normalize_code(code))
    result = dbEngine.select_scalar(stmt)
    if result is not None:
      return int(result)
  except Exception:
    return None
  return None

@lru_cache(maxsize=1)
def _etf_codes() -> set[str]:
  try:
    data = ak.fund_etf_spot_em()
    code_column = _first_existing_column(data, ['代码', '基金代码'])
    if code_column:
      return {_normalize_code(code) for code in data[code_column].dropna().tolist()}
  except Exception as e:
    logger.debug(f"Error downloading optional ETF fund list: {e}")
  return set()

@lru_cache(maxsize=1)
def _lof_codes() -> set[str]:
  try:
    data = ak.fund_lof_spot_em()
    code_column = _first_existing_column(data, ['代码', '基金代码'])
    if code_column:
      return {_normalize_code(code) for code in data[code_column].dropna().tolist()}
  except Exception as e:
    logger.debug(f"Error downloading optional LOF fund list: {e}")
  return set()

def _classify_market_by_rule(code: str, name: str = '', fund_type: str = '') -> int:
  code = _normalize_code(code)
  name = str(name or '').upper()
  fund_type = str(fund_type or '').upper()
  is_etf_link = '联接' in name or '连接' in name or '联接' in fund_type or '连接' in fund_type

  if 'LOF' in fund_type or 'LOF' in name or code.startswith(LOF_CODE_PREFIXES):
    return Define.FUND_TYPE_LOF
  if (('ETF' in fund_type or 'ETF' in name) and not is_etf_link) or code.startswith(ETF_CODE_PREFIXES):
    return Define.FUND_TYPE_ETF
  return Define.FUND_TYPE_OPEN

def get_fund_market(code: str) -> int:
  code = _normalize_code(code)
  rule_market = _classify_market_by_rule(code)
  market = _fund_market_from_db(code)
  if market is not None:
    if market == Define.FUND_TYPE_OPEN and rule_market in (Define.FUND_TYPE_ETF, Define.FUND_TYPE_LOF):
      return rule_market
    return market
  return rule_market

def _classify_market(row) -> int:
  code = _normalize_code(row.get('code', ''))
  name = str(row.get('name', ''))
  fund_type = str(row.get('基金类型', row.get('market', '')))
  return _classify_market_by_rule(code=code, name=name, fund_type=fund_type)

def download_list() -> Optional[DataFrame]:
  try:
    fund_info = ak.fund_name_em()
    if fund_info.empty:
      return None

    fund_info = fund_info.copy()
    fund_info = _rename_first_existing(fund_info, 'code', ['基金代码', '代码'])
    fund_info = _rename_first_existing(fund_info, 'name', ['基金简称', '基金名称', '名称'])
    if 'code' not in fund_info.columns or 'name' not in fund_info.columns:
      logger.warning(f"Fund list columns are invalid: {fund_info.columns.tolist()}")
      return None

    fund_info['code'] = fund_info['code'].apply(_normalize_code)
    fund_info['market'] = fund_info.apply(_classify_market, axis=1)
    fund_info['type'] = Define.TYPE_FUND
    fund_info = fund_info[['code', 'name', 'market', 'type']]

    return fund_info.drop_duplicates(subset=['code'])
  except Exception as e:
    logger.warning(f"Error downloading fund list: {e}")
  return None

def get_name(code: str) -> Optional[str]:
  return Define.get_name(Define.TYPE_FUND, code)

def _normalize_trading_history(data: DataFrame) -> DataFrame:
  data = data.copy()
  data = _rename_first_existing(data, '日期', ['净值日期'])
  data = _rename_first_existing(data, '开盘', ['开盘价'])
  data = _rename_first_existing(data, '收盘', ['最新价', '单位净值', '收盘价'])
  data = _rename_first_existing(data, '最高', ['最高价'])
  data = _rename_first_existing(data, '最低', ['最低价'])
  data = _rename_first_existing(data, '成交量', ['成交量(手)'])
  data = _rename_first_existing(data, '成交额', ['成交额(元)'])
  data = _rename_first_existing(data, '涨跌幅', ['日增长率'])
  data = _rename_first_existing(data, '涨跌额', ['日增长值'])

  for column in HISTORY_COLUMNS:
    if column not in data.columns:
      data[column] = 0.0 if column != '日期' else ''

  data = data[HISTORY_COLUMNS]
  data = _normalize_numeric_columns(data, [column for column in HISTORY_COLUMNS if column != '日期'])
  data['日期'] = pd.to_datetime(data['日期'], errors='coerce').dt.strftime('%Y-%m-%d')
  data = data.dropna(subset=['日期'])
  return data.set_index('日期')

def _open_fund_info(code: str) -> DataFrame:
  return ak.fund_open_fund_info_em(symbol=_normalize_code(code), indicator='单位净值走势')

def _normalize_open_history(data: DataFrame, start: str, end: str, period: str) -> DataFrame:
  data = data.copy()
  data = _rename_first_existing(data, '日期', ['净值日期'])
  data = _rename_first_existing(data, '单位净值', ['净值', '最新净值'])
  data = _rename_first_existing(data, '日增长率', ['涨跌幅'])
  if '日期' not in data.columns or '单位净值' not in data.columns:
    logger.warning(f"Open fund history columns are invalid: {data.columns.tolist()}")
    return _empty_history_df().set_index('日期')

  data['日期'] = pd.to_datetime(data['日期'], errors='coerce')
  data['单位净值'] = pd.to_numeric(data['单位净值'], errors='coerce')
  data['日增长率'] = pd.to_numeric(data['日增长率'], errors='coerce').fillna(0.0) if '日增长率' in data.columns else 0.0
  data = data.dropna(subset=['日期', '单位净值']).sort_values('日期')

  start_date = pd.to_datetime(start, format='%Y%m%d', errors='coerce')
  end_date = pd.to_datetime(end, format='%Y%m%d', errors='coerce')
  if pd.notna(start_date):
    data = data[data['日期'] >= start_date]
  if pd.notna(end_date):
    data = data[data['日期'] <= end_date]

  if data.empty:
    return _empty_history_df().set_index('日期')

  data['开盘'] = data['单位净值']
  data['收盘'] = data['单位净值']
  data['最高'] = data['单位净值']
  data['最低'] = data['单位净值']
  data['成交量'] = 0.0
  data['成交额'] = 0.0
  data['振幅'] = 0.0
  data['涨跌幅'] = data['日增长率']
  data['涨跌额'] = data['收盘'].diff().fillna(0.0).round(4)
  data['换手率'] = 0.0
  data['日期'] = data['日期'].dt.strftime('%Y-%m-%d')
  daily = data[HISTORY_COLUMNS].set_index('日期')
  daily = _normalize_numeric_columns(daily, [column for column in HISTORY_COLUMNS if column != '日期'])

  if period == Define.PERIOD_WEEKLY:
    return _resample_history(daily, 'W-FRI')
  if period == Define.PERIOD_MONTHLY:
    return _resample_history(daily, 'ME')
  return daily

def _resample_history(data: DataFrame, rule: str) -> DataFrame:
  if data.empty:
    return data

  frame = data.copy()
  frame.index = pd.to_datetime(frame.index)
  result = frame.resample(rule).agg({
    '开盘': 'first',
    '收盘': 'last',
    '最高': 'max',
    '最低': 'min',
    '成交量': 'sum',
    '成交额': 'sum',
    '换手率': 'sum'
  }).dropna(subset=['开盘', '收盘'])
  prev_close = result['收盘'].shift(1)
  result['涨跌额'] = (result['收盘'] - prev_close).fillna(0.0).round(4)
  result['涨跌幅'] = ((result['涨跌额'] / prev_close) * 100).fillna(0.0).round(4)
  result['振幅'] = (((result['最高'] - result['最低']) / prev_close) * 100).fillna(0.0).round(4)
  result.index = result.index.strftime('%Y-%m-%d')
  return result[HISTORY_COLUMNS[1:]]

def download_history_data(code: str, start: str, end: str, period: str = 'daily', adjust: str = None) -> Optional[DataFrame]:
  market = get_fund_market(code)
  try:
    if market == Define.FUND_TYPE_ETF:
      data = ak.fund_etf_hist_em(symbol=_normalize_code(code), period=period, start_date=start, end_date=end, adjust=adjust or '')
      return _normalize_trading_history(data) if not data.empty else None
    if market == Define.FUND_TYPE_LOF:
      data = ak.fund_lof_hist_em(symbol=_normalize_code(code), period=period, start_date=start, end_date=end, adjust=adjust or '')
      return _normalize_trading_history(data) if not data.empty else None

    data = _open_fund_info(code)
    return _normalize_open_history(data, start=start, end=end, period=period) if not data.empty else None
  except Exception as e:
    logger.warning(f"Error downloading fund history data for {code}: {e}")
  return None

def _normalize_trade_spot(data: DataFrame, codes: list[str] = None) -> DataFrame:
  data = data.copy()
  data = _rename_first_existing(data, '代码', ['基金代码'])
  data = _rename_first_existing(data, '名称', ['基金简称', '基金名称'])
  data = _rename_first_existing(data, '最新价', ['单位净值', '最新净值'])
  data = _rename_first_existing(data, '今开', ['开盘', '开盘价'])
  data = _rename_first_existing(data, '最高', ['最高价'])
  data = _rename_first_existing(data, '最低', ['最低价'])
  data = _rename_first_existing(data, '昨收', ['昨收价'])
  data = _rename_first_existing(data, '涨跌5分钟', ['5分钟涨跌'])
  data = _rename_first_existing(data, '涨跌幅60日', ['60日涨跌幅'])

  if '代码' not in data.columns or '名称' not in data.columns:
    return _empty_spot_df()

  data['代码'] = data['代码'].apply(_normalize_code)
  if codes is not None:
    code_set = {_normalize_code(code) for code in codes}
    data = data[data['代码'].isin(code_set)]

  for column in SPOT_COLUMNS:
    if column not in data.columns:
      data[column] = None if column in ['量比', '换手率', '市盈率', '市净率', '总市值', '流通市值', '涨速', '涨跌5分钟', '涨跌幅60日', '年初至今涨跌幅'] else 0.0
  if '序号' in data.columns:
    data['序号'] = range(1, len(data) + 1)

  data = data[SPOT_COLUMNS]
  numeric_columns = [column for column in SPOT_COLUMNS if column not in ['代码', '名称']]
  return _normalize_numeric_columns(data, numeric_columns)

def _call_open_spot() -> DataFrame:
  try:
    return ak.fund_open_fund_daily_em()
  except TypeError:
    return ak.fund_open_fund_daily_em(symbol='全部')

def _open_unit_columns(data: DataFrame) -> tuple[Optional[str], Optional[str]]:
  unit_columns = [str(column) for column in data.columns if '单位净值' in str(column) and '累计' not in str(column)]
  latest_columns = [column for column in unit_columns if '前' not in column]
  prev_columns = [column for column in unit_columns if '前' in column]
  latest = latest_columns[0] if latest_columns else (unit_columns[0] if unit_columns else None)
  previous = prev_columns[0] if prev_columns else (unit_columns[1] if len(unit_columns) > 1 else None)
  return latest, previous

def _normalize_open_spot(data: DataFrame, codes: list[str] = None) -> DataFrame:
  data = data.copy()
  data = _rename_first_existing(data, '代码', ['基金代码'])
  data = _rename_first_existing(data, '名称', ['基金简称', '基金名称'])
  if '代码' not in data.columns or '名称' not in data.columns:
    return _empty_spot_df()

  latest_column, previous_column = _open_unit_columns(data)
  if latest_column is None:
    return _empty_spot_df()

  data['代码'] = data['代码'].apply(_normalize_code)
  if codes is not None:
    code_set = {_normalize_code(code) for code in codes}
    data = data[data['代码'].isin(code_set)]

  latest = pd.to_numeric(data[latest_column], errors='coerce').fillna(0.0)
  previous = pd.to_numeric(data[previous_column], errors='coerce').fillna(latest) if previous_column else latest
  growth_value_column = _first_existing_column(data, ['日增长值', '涨跌额'])
  growth_rate_column = _first_existing_column(data, ['日增长率', '涨跌幅'])
  growth_value = pd.to_numeric(data[growth_value_column], errors='coerce').fillna(latest - previous) if growth_value_column else latest - previous
  growth_rate = pd.to_numeric(data[growth_rate_column], errors='coerce').fillna(0.0) if growth_rate_column else ((growth_value / previous.replace(0, pd.NA)) * 100).fillna(0.0)

  normalized = pd.DataFrame({
    '序号': range(1, len(data) + 1),
    '代码': data['代码'],
    '名称': data['名称'],
    '最新价': latest,
    '涨跌幅': growth_rate,
    '涨跌额': growth_value,
    '成交量': 0.0,
    '成交额': 0.0,
    '振幅': 0.0,
    '最高': latest,
    '最低': latest,
    '今开': latest,
    '昨收': previous,
    '量比': None,
    '换手率': None,
    '市盈率': None,
    '市净率': None,
    '总市值': None,
    '流通市值': None,
    '涨速': None,
    '涨跌5分钟': None,
    '涨跌幅60日': None,
    '年初至今涨跌幅': None
  })
  return normalized[SPOT_COLUMNS]

def download_spot_data(codes: list[str] = None) -> Optional[DataFrame]:
  try:
    normalized_codes = [_normalize_code(code) for code in codes] if codes is not None else None
    markets = {get_fund_market(code) for code in normalized_codes} if normalized_codes is not None else {
      Define.FUND_TYPE_OPEN,
      Define.FUND_TYPE_ETF,
      Define.FUND_TYPE_LOF
    }

    frames: list[DataFrame] = []
    if normalized_codes is not None:
      exchange_codes = [
        code for code in normalized_codes
        if get_fund_market(code) in (Define.FUND_TYPE_ETF, Define.FUND_TYPE_LOF)
      ]
      tx_rows = [_tx_spot_row(code, seq=index + 1) for index, code in enumerate(exchange_codes)]
      tx_rows = [row for row in tx_rows if row is not None]
      if tx_rows:
        frames.append(pd.DataFrame(tx_rows))
    elif Define.FUND_TYPE_ETF in markets:
      try:
        data = ak.fund_etf_spot_em()
        if not data.empty:
          frames.append(_normalize_trade_spot(data, normalized_codes))
      except Exception as e:
        logger.debug(f"Error downloading ETF fund spot data: {e}")
    if normalized_codes is None and Define.FUND_TYPE_LOF in markets:
      try:
        data = ak.fund_lof_spot_em()
        if not data.empty:
          frames.append(_normalize_trade_spot(data, normalized_codes))
      except Exception as e:
        logger.debug(f"Error downloading LOF fund spot data: {e}")
    if Define.FUND_TYPE_OPEN in markets:
      data = _call_open_spot()
      if not data.empty:
        frames.append(_normalize_open_spot(data, normalized_codes))

    frames = [frame for frame in frames if frame is not None and not frame.empty]
    result = pd.concat(frames, ignore_index=True) if frames else _empty_spot_df()

    if result.empty:
      return None

    result = result.drop_duplicates(subset=['代码'])
    result['序号'] = range(1, len(result) + 1)
    return result[SPOT_COLUMNS]
  except Exception as e:
    logger.warning(f"Error downloading fund spot data: {e}")
  return None
