from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import delete, inspect, select, text, update
from app.database import dbEngine
import app.database.data.utils as Utils
import app.database.data.define as Define
import app.database.data.stock as Stock
import app.database.data.index as Index


def get_name(type: int, code: str) -> Optional[str]:
  stmt = select(Define.InfoTable.name).where(Define.InfoTable.type == type).where(Define.InfoTable.code == code)
  result = dbEngine.select_scalar(stmt)
  return result[0] if result else None

def is_item_exist(type: int, code: str) -> bool:
  stmt = select(Define.InfoTable).where(Define.InfoTable.type == type).where(Define.InfoTable.code == code)
  result = dbEngine.select_scalar(stmt)
  return True if result is not None else False

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

# def get_name(type: int, code: str) -> Optional[str]:
#   if type == Define.TYPE_INDEX:
#     return Index.get_name(code)
#   elif type == Define.TYPE_STOCK:
#     return Stock.get_name(code)
#   else:
#     raise ValueError(f"Unknown type: {type}")
  
"""
download history data
"""
def update_download_records(type: int, code: str, period: str, start: str, end: str, adjust: str = None) -> Optional[int]:
  stmt = select(Define.DownloadRecordsTable) \
    .where(Define.DownloadRecordsTable.type == type) \
    .where(Define.DownloadRecordsTable.code == code) \
    .where(Define.DownloadRecordsTable.period == period)
  if type == Define.TYPE_STOCK:
    if adjust:
      stmt = stmt.where(Define.DownloadRecordsTable.adjust == adjust)
  result = dbEngine.select_scalar(stmt)
  if result:
    stmt = update(Define.DownloadRecordsTable).where(Define.DownloadRecordsTable.code == result.code and Define.DownloadRecordsTable.type == result.type).values(
      start=start,
      end=end
    )
    return dbEngine.update_stmt(stmt)
  else:
    record = Define.DownloadRecordsTable(type=type, code=code, period=period, start=start, end=end, adjust=adjust)
    return dbEngine.insert_instance(record)

def check_download_records(type: int, code: str, period: str, start: str, end: str, adjust: str = None) -> Optional[Define.DownloadRecordsTable]:
  exist = dbEngine.check_table_exist(Define.DownloadRecordsTable.__tablename__)
  if not exist:
    return None  
  stmt = select(Define.DownloadRecordsTable) \
    .where(Define.DownloadRecordsTable.type == type) \
    .where(Define.DownloadRecordsTable.code == code) \
    .where(Define.DownloadRecordsTable.period == period)
  if type == Define.TYPE_STOCK:
    if adjust:
      stmt = stmt.where(Define.DownloadRecordsTable.adjust == adjust)
  if start:
    stmt = stmt.where(Define.DownloadRecordsTable.start <= start)
  if end:
    stmt = stmt.where(Define.DownloadRecordsTable.end >= end)
  result = dbEngine.select_scalar(stmt)
  return result if result else None

def make_history_data_table_name(type: int, code: str, period: str, adjust: str = None) -> str:
  if type == Define.TYPE_STOCK:
    return f"history_stock_{period}_{adjust}_{code}"
  elif type == Define.TYPE_INDEX:
    return f"history_index_{period}_{code}"
  else:
    raise ValueError(f"Unknown type: {type}")

def download_history_data(type: int, code: str, start: str, end: str, period: str, adjust: str = None) -> int:
  if start is None:
    start = Utils.date_to_string_1(datetime.today() - timedelta(weeks=52))
  if end is None:
    end = Utils.date_to_string_1(datetime.today())
  data = None
  if type == Define.TYPE_STOCK:
    data = Stock.download_history_data(code=code, period=period, adjust=adjust, start=Utils.convert_history_date_2(start), end=Utils.convert_history_date_2(end))
  elif type == Define.TYPE_INDEX:
    data = Index.download_history_data(code=code, period=period, start=Utils.convert_history_date_2(start), end=Utils.convert_history_date_2(end))

  if data is not None:
    table_name = make_history_data_table_name(type=type, code=code, period=period, adjust=adjust)
    data.to_sql(table_name, dbEngine.engine, if_exists='replace', index=True, index_label='日期')

    update_download_records(type, code, period, adjust, start, end)

    return len(data)
  else:
    return 0

def fetch_history_data(type1: int, code: str, start: str, end: str, period: str, adjust: str = None, limit: int = None) -> list[Define.HistoryData]:
  table_name = make_history_data_table_name(type=type1, code=code, period=period, adjust=adjust)

  if start and end:
    stmt = text(f"SELECT * FROM {table_name} WHERE 日期 >= '{start}' AND 日期 <= '{end}' ORDER BY 日期 ASC")
  elif start:
    stmt = text(f"SELECT * FROM {table_name} WHERE 日期 >= '{start}' ORDER BY 日期 ASC")
  elif end:
    stmt = text(f"SELECT * FROM {table_name} WHERE 日期 <= '{end}' ORDER BY 日期 ASC")
  else:
    stmt = text(f"SELECT * FROM {table_name} ORDER BY 日期 ASC")

  rows = dbEngine.select_stmt(stmt)
  # results = []
  # for row in rows:
  #   results.append(Define.HistoryData.model_validate(row._asdict()))
  results = [Define.HistoryData.model_validate(row._asdict()) for row in rows]
  if limit:
    return results[-limit:] 
  return results

def get_history_data(type: int, code: str, start: str, end: str, period: str, adjust: str = None, limit: int = None) -> list[Define.HistoryData]:
  checked = check_download_records(type=type, code=code, period=period, adjust=adjust, start=start, end=end)
  if checked is None:
    download_history_data(type=type, code=code, start=start, end=end, period=period, adjust=adjust)
  return fetch_history_data(type1=type, code=code, start=start, end=end, period=period, adjust=adjust, limit=limit)

def get_latest_history_data(type: int, code: str, period: str, adjust: str) -> Optional[Define.HistoryData]:
  # date = datetime.today()
  # while not Utils.is_workday(date):
  #   date = date - timedelta(days=1)
  date = Utils.get_latest_workday()
  start = Utils.date_to_string_1(date - timedelta(weeks=1))
  end = Utils.date_to_string_1(date)
  results = get_history_data(type=type, code=code, start=start, end=end, period=period, adjust=adjust, limit=1)
  if len(results) > 0:
    return results.pop()
  return None

def remove_all_history_data() -> int:
  dbEngine.trunc_table(Define.DownloadRecordsTable)

  inspector = inspect(dbEngine.engine)
  table_names = inspector.get_table_names()

  table_names = [table_name for table_name in table_names if table_name.startswith("history_")]
  count = 0
  for table_name in table_names:
    stmt = text(f"DROP TABLE IF EXISTS {table_name}")
    dbEngine.execute_stmt(stmt)
    count += 1

  return count

"""
get spot data
"""
def get_spot_data(type: int, codes: list[str] = None) -> list[Define.SpotData]:
  if codes is None and len(codes) == 0:
    return []
  
  if type == Define.TYPE_STOCK:
    data = Stock.download_spot_data(codes=codes)
  elif type == Define.TYPE_INDEX:
    data = Index.download_spot_data(codes=codes)
  else:
    raise ValueError(f"Unknown type: {type}")
  if data is not None:
    results = [Define.SpotData.model_validate(row) for row in data.to_dict(orient='records')]
    return results
  return []
