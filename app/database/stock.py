"""
股票类常用函数封装
"""
from pandas import DataFrame
from app.database import common, tables

def get_a_list() -> DataFrame:
  return common.select(tables.TableName.Stock_A_List)

def get_history(code: str, start: str = None, end: str = None, columns: list[str] = None, peroid: str = 'daily', adjust: str = 'qfq') -> DataFrame:
  table = tables.TableName.make_stock_history_name(code, peroid, adjust)
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

# def get_history_by_date(code: str, date: str = None, columns: list[str] = None, peroid: str = 'daily', adjust: str = 'qfq') -> DataFrame:
#   table = tables.TableName.make_stock_history_name(code, peroid, adjust)
#   where = None
#   if date:
#       where = f'WHERE 日期 == "{date} LIMIT 1'
#   else:
#      where = f'ORDER BY 日期 DESC LIMIT 1'

#   return common.select(table, columns, where)
