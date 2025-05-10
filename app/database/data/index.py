from typing import Optional
from pandas import DataFrame
from sqlalchemy import delete
from app.database.data import define as Define, utils as Utils
from app.database import dbEngine
import akshare as ak
"""
Index
"""
def download_list() -> None:
  stmt = delete(Define.InfoTable).where(Define.InfoTable.type == Define.TYPE_INDEX)
  dbEngine.delete_stmt(stmt)
  # download
  index_info = ak.index_stock_info()
  if not index_info.empty:
    index_info = index_info.drop(columns=['publish_date'], axis=1)
    index_info = index_info.rename(columns={
      'index_code': 'code',
      'display_name': 'name'
    })
    index_info['market'] = index_info['code'].apply(lambda x: 'sh' if x.startswith('000') else 'sz')  
    index_info['type'] = Define.TYPE_INDEX
  data = index_info.to_dict(orient='records')
  dbEngine.bulk_insert_data(Define.InfoTable, data)

def get_name(code: str) -> Optional[str]:
  return Define.get_name(Define.TYPE_INDEX, code)

def download_history_data(code: str, start: str, end: str, period: str = 'daily') -> Optional[DataFrame]:
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