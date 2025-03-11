from sqlalchemy import Column, Float, ForeignKey, ForeignKeyConstraint, Index, Integer, String, DateTime, select
from sqlalchemy.sql import func
from app.database import dbEngine, TableBase

HOLDING_FLAG_ACTIVE: int = 0
HOLDING_FLAG_REMOVED: int = 1
OPERATION_ACTION_BUY: int = 0
OPERATION_ACTION_SELL: int = 1

class UserHoldingTable(TableBase):
  __tablename__ = 'user_holding_table'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  uid = Column(Integer, nullable=False, default=99)
  type = Column(Integer, nullable=False, default=1)
  code = Column(String, nullable=False)
  flag = Column(Integer, nullable=False, default=HOLDING_FLAG_ACTIVE)
  created = Column(DateTime(timezone=True), server_default=func.now())
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  __table_args__ = (
      Index('idx_user_holding_type_code', 'type', 'code'),
  )

class UserHoldingOperationTable(TableBase):
  __tablename__ = 'user_holding_operation_table'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  holding = Column(Integer, ForeignKey(UserHoldingTable.id), nullable=False)
  action = Column(Integer, nullable=False)
  quantity = Column(Integer, nullable=False)
  price = Column(Float, nullable=False)
  expense = Column(Float, nullable=False)
  comment = Column(String, nullable=True)
  created = Column(DateTime(timezone=True), server_default=func.now())

def insert_holding(uid: int, type: int, code: str) -> int:
  return dbEngine.insert_instance(UserHoldingTable(uid=uid, type=type, code=code))

def insert_operation(id: int, action: int, quantity: int, price: float, expense: float, comment: str = None) -> int:
  return dbEngine.insert_instance(UserHoldingOperationTable(holding=id, action=action, quantity=quantity, price=price, expense=expense, comment=comment))

def select_holding(uid: int, type: int = -1, code: str = None) -> list[UserHoldingTable]:
  stmt = select(UserHoldingTable).where(UserHoldingTable.uid == uid)
  if type != -1:
    stmt = stmt.where(UserHoldingTable.type == type)
  if code: 
    stmt = stmt.where(UserHoldingTable.code == code)
  return dbEngine.select_stmt(stmt)
