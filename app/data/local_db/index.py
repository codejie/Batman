"""
Index本地化函数
"""
from pandas import DataFrame

from app.utils import utils
from app.data.remote_api import index as remote
from app.database import tables, dbEngine

"""
获取A股指数
"""
def fetch_a_list(if_exists: str = 'replace') -> None:
  df = remote.get_infos()
  if not df.empty:
    df = df.drop(columns=['publish_date'], axis=1)
    df = df.rename(columns={
      'index_code': 'code',
      'dispaly_name': 'name'
    })
    df['market'] = 'sh' if df['code'].str.startswith('000') == True else 'sz'
    df.to_sql(tables.TableName.Index_A_List, dbEngine.get_engine(), if_exists=if_exists, index=False)

"""
获取指数历史数据
"""    
def get_history(symbol: str, start_date: str, end_date: str, period: str = 'daily', adjust: str = 'qfq') -> DataFrame:
  pass
