"""
Table & structure definitions
"""
from typing import Optional
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
  id = Column(Integer, primary_key=True, autoincrement=True)
  type = Column(Integer, nullable=False)
  code = Column(String, nullable=False)
  period = Column(String, nullable=False)
  adjust = Column(String, nullable=True)
  start = Column(String, nullable=False)
  end = Column(String, nullable=False)
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  __table_args__ = (
    # PrimaryKeyConstraint('type', 'code', name='pk_download_records_type_code'),
    Index('idx_download_records_type_code', 'type', 'code'),
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

  # class Config:
  #   from_attributes = True

"""
Spot Data Model
"""
class SpotData(BaseModel):
  序号: int
  代码: str
  名称: str
  最新价: float
  涨跌幅: float
  涨跌额: float
  成交量: float
  成交额: float
  振幅: float
  最高: float
  最低: float
  今开: float
  昨收: float
  量比: float
  换手率: Optional[float] = None
  市盈率: Optional[float] = None
  市净率: Optional[float] = None
  总市值: Optional[float] = None
  流通市值: Optional[float] = None
  涨速: Optional[float] = None
  涨跌5分钟: Optional[float] = None
  涨跌幅60日: Optional[float] = None
  年初至今涨跌幅: Optional[float] = None

  def to_dict(self):
    return {
      '序号': self.序号,
      '代码': self.代码,
      '名称': self.名称,
      '最新价': self.最新价,
      '涨跌幅': self.涨跌幅,
      '涨跌额': self.涨跌额,
      '成交量': self.成交量,
      '成交额': self.成交额,
      '振幅': self.振幅,
      '最高': self.最高,
      '最低': self.最低,
      '今开': self.今开,
      '昨收': self.昨收,
      '量比': self.量比,
      '换手率': self.换手率,
      '市盈率': self.市盈率,
      '市净率': self.市净率,
      '总市值': self.总市值,
      '流通市值': self.流通市值,
      '涨速': self.涨速,
      '涨跌5分钟': self.涨跌5分钟,
      '涨跌幅60日': self.涨跌幅60日,
      '年初至今涨跌幅': self.年初至今涨跌幅      
    }

  # class Config:
  #   from_attributes = True

