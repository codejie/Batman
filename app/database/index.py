"""
指数类常用函数封装
"""
from pandas import DataFrame
from app.database import common, tables

def get_a_list() -> DataFrame:
  return common.select(tables.TableName.Index_A_List)

def get_info(code: str) -> DataFrame:
  return common.select(table=tables.TableName.Index_A_List, columns=['code', 'name', 'market'], where=f'WHERE code="{code}"')

def get_history(code: str, start: str = None, end: str = None, columns: list[str] = None, period: str = 'daily') -> DataFrame:
  table = tables.TableName.make_index_history_name(code, period)
  where = None
  if start and end:
    where = f'WHERE 日期 >="{start}" AND 日期 <= "{end}" order by 日期'
  elif start:
     where = f'WHERE 日期 >="{start}" order by 日期'
  elif end:
     where = f'日期 <= "{end}" order by 日期'
  else:
     where = f'ORDER BY 日期 DESC LIMIT 1'
  return common.select(table, columns, where)