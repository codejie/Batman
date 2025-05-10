"""
Stock
"""
from typing import Optional
from pandas import DataFrame
import akshare as ak
from sqlalchemy import delete
from app.database import dbEngine
from app.database.data import define as Define
from app.database.data import utils as Utils

def download_list() -> None:
  # delete
  stmt = delete(Define.InfoTable).where(Define.InfoTable.type == Define.TYPE_STOCK)
  dbEngine.delete_stmt(stmt)
  # download
  stock_info = ak.stock_info_a_code_name()
  stock_info['type'] = Define.TYPE_STOCK
  stock_info['market'] = None
  data = stock_info.to_dict(orient='records')
  dbEngine.bulk_insert_data(Define.InfoTable, data)

def get_name(code: str) -> Optional[str]:
  return Define.get_name(Define.TYPE_STOCK, code)

def download_history_data(code: str, start: str, end: str, period: str = 'daily', adjust: str = None) -> Optional[DataFrame]:
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
  return None
