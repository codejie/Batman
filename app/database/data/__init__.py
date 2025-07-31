from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import delete, inspect, or_, select, text, update
from app.database import dbEngine
import app.database.data.utils as Utils
import app.database.data.define as Define
import app.database.data.stock as Stock
import app.database.data.index as Index


def get_name(type: int, code: str) -> Optional[str]:
  stmt = select(Define.InfoTable.name).where(Define.InfoTable.type == type).where(Define.InfoTable.code == code)
  result = dbEngine.select_scalar(stmt)
  return result if result else None

def get_item_info(type: int, key: str) -> Optional[Define.ItemInfo]:
  stmt = select(Define.InfoTable).where(Define.InfoTable.type == type).where(or_(Define.InfoTable.name == key, Define.InfoTable.code == key))
  result = dbEngine.select_scalar(stmt)
  if result:
    return Define.ItemInfo(type=result.type, code=result.code, name=result.name)

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

def download_history_data(type: int, code: str, start: str, end: str, period: str, adjust: str = None, record_flag: int = Define.RECORD_FLAG_NORMAL) -> int:
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

    if record_flag != Define.RECORD_FLAG_DISABLED:
      update_download_records(type=type, code=code, period=period, adjust=adjust, start=start, end=end)

    return len(data)
  else:
    return 0

def fetch_history_data(type: int, code: str, start: str, end: str, period: str, adjust: str = None, limit: int = None) -> list[Define.HistoryData]:
  table_name = make_history_data_table_name(type=type, code=code, period=period, adjust=adjust)

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

def get_history_data(type: int, code: str, start: str, end: str, period: str, adjust: str = None, limit: int = None, record_flag: int = Define.RECORD_FLAG_NORMAL) -> list[Define.HistoryData]:
  checked = check_download_records(type=type, code=code, period=period, adjust=adjust, start=start, end=end) if record_flag != Define.RECORD_FLAG_DISABLED else None
  if checked is None:
    download_history_data(type=type, code=code, start=start, end=end, period=period, adjust=adjust, record_flag=record_flag)
  return fetch_history_data(type=type, code=code, start=start, end=end, period=period, adjust=adjust, limit=limit)

def get_latest_history_data(type: int, code: str, period: str, adjust: str, limit: int = None, record_flag: int = Define.RECORD_FLAG_DISABLED) -> Optional[Define.HistoryData] | Optional[list[Define.HistoryData]]:
  # date = datetime.today()
  # while not Utils.is_workday(date):
  #   date = date - timedelta(days=1)
  date = Utils.get_latest_workday()
  start = Utils.date_to_string_1(date - timedelta(weeks=1))
  end = Utils.date_to_string_1(date)
  results = get_history_data(type=type, code=code, start=start, end=end, period=period, adjust=adjust, limit=(limit if limit else 1), record_flag=record_flag)
  if len(results) > 0:
    if limit:
      return results[-limit:]
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

def get_spot_data_use_history(type: int, codes: list[str] = None) -> list[Define.SpotData]:
  if codes is None and len(codes) == 0:
    return []
  
  date = Utils.get_latest_workday()
  start = Utils.date_to_string_1(date - timedelta(weeks=1))
  end = Utils.date_to_string_1(date)

  results: list[Define.SpotData] = []
  for code in codes:
    ret = get_history_data(type=type, code=code, start=start, end=end, period='daily', adjust='qfq', limit=1, record_flag=Define.RECORD_FLAG_DISABLED)
    if len(ret) > 0:
      history = ret.pop()
      results.append(Define.SpotData(
        序号=0,
        代码=code,
        名称='',
        最新价=history.收盘,
        涨跌额=history.涨跌额,
        涨跌幅=history.涨跌幅,
        成交量=history.成交量,
        成交额=history.成交额,
        振幅=history.振幅,
        最高=history.最高,
        最低=history.最低,
        今开=history.开盘,
        昨收=history.开盘,
        换手率=history.换手率
      ))

  return results
