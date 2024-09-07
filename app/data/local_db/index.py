"""
Index本地化函数
"""
from datetime import datetime
from pandas import DataFrame
import pandas

from app.utils import utils
from app.data.remote_api import index as remote
from app.database import tables, dbEngine

"""
获取/下载A股指数
"""
def fetch_a_list(if_exists: str = 'replace') -> None:
  df = remote.get_infos()
  if not df.empty:
    df = df.drop(columns=['publish_date'], axis=1)
    df = df.rename(columns={
      'index_code': 'code',
      'display_name': 'name'
    })
    df['market'] = df['code'].apply(lambda x: 'sh' if x.startswith('000') else 'sz')
    df.to_sql(tables.TableName.Index_A_List, dbEngine.get_engine(), if_exists=if_exists, index=False)

"""
获取指数列表
"""
def get_a_list() -> DataFrame:
  return pandas.read_sql_table(tables.TableName.Index_A_List, dbEngine.get_engine())

"""
获取指数历史数据
"""    
def fetch_history(code: str, start: datetime, end: datetime, period: str = 'daily',  if_exists='replace') -> None:
  start = utils.date2String1(start)
  end = utils.date2String1(end)
  df = remote.get_history(code, start, end, period)
  if not df.empty:
    table = tables.TableName.make_index_history_name(code, period)
    df.to_sql(name=table, con=dbEngine.get_engine(), if_exists=if_exists, index=False)
