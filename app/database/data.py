"""
Data
"""

from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, Index, Integer, PrimaryKeyConstraint, String, func, inspect, select, text
from app.database import TableBase, dbEngine
import akshare as ak


TYPE_INDEX: int = 1
TYPE_STOCK: int = 2

"""
Stock & Index Information Table
"""

class InfoTable(TableBase):
  __tablename__ = 'item_info_table'

  type = Column(Integer, nullable=False, default=TYPE_STOCK)
  code = Column(String, nullable=False)
  name = Column(String, nullable=False)
  market = Column(Integer, nullable=True, default=0)

  __table_args__ = (
      PrimaryKeyConstraint('type', 'code', name='pk_info_type_code'),
  )

def select_name(code: str, type: int = TYPE_STOCK) -> Optional[str]:
  stmt = select(InfoTable.name, InfoTable.type).where(InfoTable.type == type).where(InfoTable.code == code)
  result = dbEngine.select_scalar(stmt)
  return result[0] if result else None

"""
download stock info with AKShare
"""
def download_stock_info():
  stock_info = ak.stock_info_a_code_name()
  stock_info['type'] = TYPE_STOCK
  stock_info['market'] = None
  data = stock_info.to_dict(orient='records')
  dbEngine.bulk_insert_data(InfoTable, data)

"""
Stock & Index download records
"""
class DownloadRecordsTable(TableBase):
  __tablename__ = 'item_download_records'
  id = Column(Integer, primary_key=True)
  type = Column(Integer, nullable=False, default=TYPE_STOCK)
  code = Column(String, nullable=False)
  period = Column(String, nullable=False)
  adjust = Column(String, nullable=False)
  start = Column(String, nullable=False)
  end = Column(String, nullable=False)
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  __table_args__ = (
    Index('idx_download_records_type_code', 'type', 'code'),
  )

def update_download_records(type: int, code: str, period: str, adjust: str, start: str, end: str) -> Optional[int]:
  stmt = select(DownloadRecordsTable).where(DownloadRecordsTable.type == type).where(DownloadRecordsTable.code == code).where(DownloadRecordsTable.period == period).where(DownloadRecordsTable.adjust == adjust)
  result = dbEngine.select_scalar(stmt)
  if result:
    return result.id
  else:
    record = DownloadRecordsTable(type=type, code=code, period=period, adjust=adjust, start=start, end=end)
    return dbEngine.insert_instance(record)

def check_download_records(type: int, code: str, period: str, adjust: str, start: str, end: str) -> Optional[DownloadRecordsTable]:
  stmt = select(DownloadRecordsTable).where(DownloadRecordsTable.type == type).where(DownloadRecordsTable.code == code).where(DownloadRecordsTable.period == period).where(DownloadRecordsTable.adjust == adjust)
  result = dbEngine.select_scalar(stmt)
  if result:
    return result
  return result if result else None

"""
Data common classes and functions
"""
# history_table_map = {}

class HistoryData(BaseModel):
  日期: str
  开盘: float
  收盘: float
  最高: float
  最低: float
  成交量: float
  成交额: float
  振幅: float
  涨跌幅: float
  涨跌额: float
  换手率: float


def make_history_data_table_name(type: int, code: str, period: str, adjust: str) -> str:
  if type == TYPE_STOCK:
    return f"stock_{period}_{adjust}_{code}"
  elif type == TYPE_INDEX:
    return f"index_{period}_{adjust}_{code}"

def download_history_data(type: int, code: str, start: str, end: str, period: str = 'daily', adjust: str = 'qfq') -> int:
  data = None
  if type == TYPE_STOCK:
    data = ak.stock_zh_a_hist(symbol=code, period=period, adjust=adjust, start_date=start, end_date=end)
  elif type == TYPE_INDEX:
    data = None

  if data is not None:
    data = data.drop('股票代码', axis=1)
    table_name = make_history_data_table_name(type, code, period, adjust)
    data.set_index('日期', inplace=True)
    data.to_sql(table_name, dbEngine.engine, if_exists='replace', index=True, index_label='日期')

    return len(data)
  else:
    return 0
  
# def make_history_data_table(type: int, code: str, period: str, adjust: str) -> str:
#   table_name = make_history_data_table_name(type, code, period, adjust)
#   class DynamicTable(TableBase):
#     __tablename__ = table_name
#     # id = Column('index', Integer, autoincrement=True, primary_key=True)
#     date = Column('日期', DateTime, nullable=True)
#     open = Column('开盘', Float, nullable=True)
#     close = Column('收盘', Float, nullable=True)
#     high = Column('最高', Float, nullable=True)
#     low = Column('最低', Float, nullable=True)
#     volume = Column('成交量', Float, nullable=True)
#     amount = Column('成交额', Float, nullable=True)
#     amplitude = Column('振幅', Float, nullable=True)
#     change_pct = Column('涨跌幅', Float, nullable=True)
#     change = Column('涨跌额', Float, nullable=True)
#     turnover_rate = Column('换手率', Float, nullable=True)

#     __table_args__ = (
#       PrimaryKeyConstraint('日期', name=f'pk_{__tablename__}_date'),
#       # Index(f"idx_{__tablename__}_date", '日期'),
#     )

#   inspector = inspect(dbEngine.engine)
#   if not inspector.has_table(table_name):
#     DynamicTable.__table__.create(dbEngine.engine)
#   # history_table_map[table_name] = DynamicTable

#   return table_name

# def truncate_table(table: TableBase) -> TableBase:
#   table.__table__.drop(dbEngine.engine, checkfirst=True)
#   table.__table__.create(dbEngine.engine)
#   return table

# def get_history_data_table(type: int, code: str, period: str, adjust: str) -> TableBase:
#   table_name = make_history_data_table_name(type, code, period, adjust)
#   if table_name in histtory_table_map:
#     return histtory_table_map[table_name]
#   else:
#     table = make_history_data_table(type, code, period, adjust)
#     histtory_table_map[table_name] = table
#     return table

def fetch_history_data(type: int, code: str, start: str, end: str, period: str, adjust: str) -> list[HistoryData]:
  table_name = make_history_data_table_name(type, code, period, adjust)
  inspector = inspect(dbEngine.engine)
  if not inspector.has_table(table_name):
    return []

  if start and end:
    stmt = text(f"SELECT * FROM {table_name} WHERE 日期 >= '{start}' AND 日期 <= '{end}' ORDER BY 日期 DESC")
  elif start:
    stmt = text(f"SELECT * FROM {table_name} WHERE 日期 >= '{start}' ORDER BY 日期 DESC")
  elif end:
    stmt = text(f"SELECT * FROM {table_name} WHERE 日期 <= '{end}' ORDER BY 日期 DESC")
  else:
    stmt = text(f"SELECT * FROM {table_name} ORDER BY 日期 DESC")

  result = dbEngine.select_stmt(stmt)
  return result
