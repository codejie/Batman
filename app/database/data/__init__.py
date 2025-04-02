from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import delete, select, text, update
from app.database import TableBase, dbEngine
import akshare as ak
import app.database.data.utils as Utils
import app.database.data.define as Define
import app.database.data.stock as Stock
import app.database.data.index as Index


def get_name(type: int, code: str) -> Optional[str]:
  stmt = select(Define.InfoTable.name, Define.InfoTable.type).where(Define.InfoTable.type == type).where(Define.InfoTable.code == code)
  result = dbEngine.select_scalar(stmt)
  return result[0] if result else None

"""
download info list
"""
def download_list(type: int) -> None:
  stmt = delete(Define.InfoTable).where(Define.InfoTable.type == type)
  dbEngine.delete_stmt(stmt)
  if type == Define.TYPE_STOCK:
    Stock.download_list()
  elif type == Define.TYPE_INDEX:
    Index.download_list()
  else:
    raise ValueError(f"Unknown type: {type}")

def get_name(type: int, code: str) -> Optional[str]:
  if type == Define.TYPE_INDEX:
    return Index.get_name(code)
  elif type == Define.TYPE_STOCK:
    return Stock.get_name(code)
  else:
    raise ValueError(f"Unknown type: {type}")

def update_download_records(type: int, code: str, period: str, adjust: str, start: str, end: str) -> Optional[int]:
  stmt = select(Define.DownloadRecordsTable) \
    .where(Define.DownloadRecordsTable.type == type
           and Define.DownloadRecordsTable.code == code
           and Define.DownloadRecordsTable.period == period
           and Define.DownloadRecordsTable.adjust == adjust)
  result = dbEngine.select_scalar(stmt)
  if result:
    stmt = update(Define.DownloadRecordsTable).where(Define.DownloadRecordsTable.code == result.code and Define.DownloadRecordsTable.type == result.type).values(
      start=start,
      end=end
    )
    return dbEngine.update_stmt(stmt)
  else:
    record = Define.DownloadRecordsTable(type=type, code=code, period=period, adjust=adjust, start=start, end=end)
    return dbEngine.insert_instance(record)

def check_download_records(type: int, code: str, period: str, adjust: str, start: str, end: str) -> Optional[Define.DownloadRecordsTable]:
  stmt = select(Define.DownloadRecordsTable) \
    .where(Define.DownloadRecordsTable.type == type
           and Define.DownloadRecordsTable.code == code
           and Define.DownloadRecordsTable.period == period
           and Define.DownloadRecordsTable.adjust == adjust)
  if start:
    stmt = stmt.where(Define.DownloadRecordsTable.start <= start)
  if end:
    stmt = stmt.where(Define.DownloadRecordsTable.end >= end)
  result = dbEngine.select_scalar(stmt)
  return result if result else None

def make_history_data_table_name(type: int, code: str, period: str, adjust: str) -> str:
  if type == Define.TYPE_STOCK:
    return f"stock_{period}_{adjust}_{code}"
  elif type == Define.TYPE_INDEX:
    return f"index_{period}_{adjust}_{code}"
  else:
    raise ValueError(f"Unknown type: {type}")

def download_history_data(type: int, code: str, start: str, end: str, period: str = 'daily', adjust: str = 'qfq') -> int:
  data = None
  if type == Define.TYPE_STOCK:
    data = Stock.download_history_data(code=code, period=period, adjust=adjust, start=Utils.convert_history_date_2(start), end=Utils.convert_history_date_2(end))
  elif type == Define.TYPE_INDEX:
    data = None

  if data is not None:
    table_name = make_history_data_table_name(type, code, period, adjust)
    data.to_sql(table_name, dbEngine.engine, if_exists='replace', index=True, index_label='日期')

    update_download_records(type, code, period, adjust, start, end)

    return len(data)
  else:
    return 0

def fetch_history_data(type: int, code: str, start: str, end: str, period: str, adjust: str, limit: int = None) -> list[Define.HistoryData]:
  table_name = make_history_data_table_name(type, code, period, adjust)

  if start and end:
    stmt = text(f"SELECT * FROM {table_name} WHERE 日期 >= '{start}' AND 日期 <= '{end}' ORDER BY 日期 ASC")
  elif start:
    stmt = text(f"SELECT * FROM {table_name} WHERE 日期 >= '{start}' ORDER BY 日期 ASC")
  elif end:
    stmt = text(f"SELECT * FROM {table_name} WHERE 日期 <= '{end}' ORDER BY 日期 ASC")
  else:
    stmt = text(f"SELECT * FROM {table_name} ORDER BY 日期 ASC")

  results = dbEngine.select_stmt(stmt)
  if limit:
    return results[-limit:] 
  return results

def get_history_data(type: int, code: str, start: str, end: str, period: str, adjust: str, limit: int = None) -> list[Define.HistoryData]:
  checked = check_download_records(type, code, period, adjust, start, end)
  if not checked:
    download_history_data(type, code, start, end, period, adjust)
  return fetch_history_data(type, code, start, end, period, adjust, limit)

def get_latest_history_data(type: int, code: str, period: str, adjust: str) -> Optional[Define.HistoryData]:
  # date = datetime.today()
  # while not Utils.is_workday(date):
  #   date = date - timedelta(days=1)
  date = Utils.get_latest_workday()
  start = Utils.date_to_string_1(date - timedelta(weeks=52))
  end = Utils.date_to_string_1(date)
  results = get_history_data(type, code, start, end, period, adjust, 1)
  if len(results) > 0:
    return results.pop()
  return None
