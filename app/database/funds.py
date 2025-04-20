from pandas import Index
from sqlalchemy import Column, Integer
from app.database import TableBase


class FundsTables(TableBase):
  __tablename__ = 'funds_table'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
  uid = Column(Integer, nullable=False, default=99)
  total = Column(float, nullable=False, default=0)
  avaliable = Column(float, nullable=False, default=0)

  __table_args__ = (
    Index('idx_funds_uid', 'uid'),
  )