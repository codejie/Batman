from app.database import TableBase, Column, Integer, Float, String, DateTime, func


class HoldingListTable(TableBase):
  __tablename__ = 'user_holding_list'

  id = Column(Integer, autoincrement=True, primary_key=True)
  uid = Column(Integer, nullable=False, default=99)
  type = Column(Integer, default=1)
  code = Column(String, nullable=False)
  quantity = Column(Integer, nullable=False)
  buying = Column(Float, nullable=False)
  cost = Column(Float, nullable=False)
  comment = Column(String, nullable=True)
  created = Column(DateTime(timezone=True), server_default=func.now())
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

class TradeRecordsTable(TableBase):
  __tablename__ = 'user_trade_records'

  id = Column(Integer, autoincrement=True, primary_key=True)
  uid = Column(Integer, nullable=False, default=99)
  action = Column(Integer, nullable=False)
  type = Column(Integer, default=1)
  code = Column(String, nullable=False)
  quantity = Column(Integer, nullable=False)
  buying = Column(Float, nullable=False)
  selling = Column(Float, nullable=False)
  cost = Column(Float, nullable=False)
  comment = Column(String, nullable=True)
  created = Column(DateTime(timezone=True), server_default=func.now())
