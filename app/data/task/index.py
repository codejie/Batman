from datetime import datetime

from pandas import DataFrame
from app.data.local_db import index as local
from app.data.task import records
from app.exception import AppException
from app.logger import logger
from app.database import dbEngine, sql_select, func, tables
from app.logger import logger

"""
init check
"""
def init_check() -> None:
  try:
    if not exist_list_table():
      start = records.HISTORY_START
      end = datetime.now()
      init_list(start, end)

      symbols = get_list()

      init_daily_history(symbols=symbols, start=start, end=end)
  except Exception as e:
    raise AppException(e)
  
def exist_list_table() -> bool:
  stmt = sql_select(func.count()).select_from(tables.IndexAListTable)
  result = dbEngine.select_one(stmt)
  return result > 0

def init_list(start: datetime, end: datetime) -> None:
  local.fetch_a_list(if_exists='replace')
  records.insert(records.Item.INDEX_LIST, end)

def get_list() -> DataFrame:
  return local.get_a_list()

def init_daily_history(symbols: DataFrame, start: datetime, end: datetime) -> None:

  for i, r in symbols.iterrows():
    code = r['code']
    try:
      local.fetch_history(code, start, end, if_exists='replace')
      records.insert(records.Item.INDEX_DAILY_HISTORY, end, code)
    except AppException as e:
      logger.warning(f'init index {code} history fail - {e.message}')
"""
daily update
"""
def update_daily() -> None:
  try:
    symbols = get_list()
    update_daily_history(symbols=symbols)
  except Exception as e:
    raise AppException(e)
  
def update_daily_history(symbols: DataFrame) -> None:
  for i, r in symbols.iterrows():
    code = r['code']
    start, end, is_update = records.get_start_end(records.Item.INDEX_DAILY_HISTORY, code)
    if start < end:
      try:
        local.fetch_history(code, start, end, if_exists='replace')
        records.set_latest(records.Item.INDEX_DAILY_HISTORY, end, code, is_update)
      except AppException as e:
        logger.warning(f'update {code} history fail - {e.message}')