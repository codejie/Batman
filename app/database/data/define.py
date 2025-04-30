"""
Table & structure definitions
"""
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Index, Integer, PrimaryKeyConstraint, String, func
from app.database import TableBase

TYPE_INDEX: int = 1
TYPE_STOCK: int = 2

PERIOD_DAILY: str = 'daily'
PERIOD_WEEKLY: str = 'weekly'
PERIOD_MONTHLY: str = 'monthly'

ADJUST_QFQ: str = 'qfq'

"""
Data Options
"""
dataOptions = {
  'offline': False
}

"""
Stock & Index Information Table
"""
class InfoTable(TableBase):
  __tablename__ = 'item_info_table'

  type = Column(Integer, nullable=False)
  code = Column(String, nullable=False)
  name = Column(String, nullable=False)
  market = Column(Integer, nullable=True, default=0)

  __table_args__ = (
      PrimaryKeyConstraint('type', 'code', name='pk_info_type_code'),
  )

"""
Stock & Index download records
"""
class DownloadRecordsTable(TableBase):
  __tablename__ = 'item_download_records'
  # id = Column(Integer, primary_key=True, autoincrement=True)
  type = Column(Integer, nullable=False)
  code = Column(String, nullable=False)
  period = Column(String, nullable=False)
  adjust = Column(String, nullable=True)
  start = Column(String, nullable=False)
  end = Column(String, nullable=False)
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  __table_args__ = (
    PrimaryKeyConstraint('type', 'code', name='pk_download_records_type_code'),
    # Index('idx_download_records_type_code', 'type', 'code'),
  )

"""
History Data Model
"""
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

  class Config:
    from_attributes = True
