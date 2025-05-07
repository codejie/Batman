from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, String, func, select, update as sql_update
from app.database import TableBase, dbEngine

FUNDS_STOCK: int = 1
# OPERATION_ACTION_IN: int = 1
# OPERATION_ACTION_OUT: int = 2

class FundsTable(TableBase):
  __tablename__ = 'funds_table'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
  uid = Column(Integer, nullable=False, default=99)
  type = Column(Integer, nullable=False, default=FUNDS_STOCK)
  amount = Column(Float, nullable=False, default=0)
  available = Column(float, nullable=False, default=0)
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  __table_args__ = (
    Index('idx_funds_uid', 'uid'),
    Index('idx_funds_type', 'type'),
  )

class FundsOperationTable(TableBase):
  __tablename__ = 'funds_operation_table'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
  funds = Column(Integer, ForeignKey(FundsTable.id), nullable=False)
  # action = Column(Integer, nullable=False) # 1: buy; 2: sell
  amount = Column(Float, nullable=False) # 入正；出负
  comment = Column(String, nullable=True)
  created = Column(DateTime(timezone=True), server_default=func.now())

"""
Functions
"""
def get(uid: int, type: int = FUNDS_STOCK) -> FundsTable | None:
  stmt = select(FundsTable).where(FundsTable.uid == uid).where(FundsTable.type == type)
  result = dbEngine.select_scalar(stmt)
  if result is None:
    return None
  return result

def insert(uid: int, amount: float, type: int = FUNDS_STOCK) -> int:
  return dbEngine.insert_instance(FundsTable(uid=uid, type=type, amount=amount, available=amount))

def update(uid: int, type: int, amount: float) -> int:
  stmt = sql_update(FundsTable) \
   .where(FundsTable.type == type) \
   .where(FundsTable.uid == uid) \
  .values(amount=func.coalesce(FundsTable.amount, 0) + amount, available=func.coalesce(FundsTable.available, 0) + amount, updated=func.now())
  return dbEngine.update_stmt(stmt)

def insert_operation(funds: int, amount: float, comment: str = None) -> int:
  return dbEngine.insert_instance(FundsOperationTable(funds=funds, amount=amount, comment=comment))

def get_operation(uid: int, funds: int) -> list[FundsOperationTable]:
  stmt = select(FundsOperationTable).where(FundsOperationTable.uid == uid).where(FundsOperationTable.funds == funds)
  return dbEngine.select_stmt(stmt)

"""
Combination
"""
def update_funds(uid: int, amount: float, type: int = FUNDS_STOCK, comment: str = None) -> int:
  funds = get(uid=uid, type=type)
  id = None
  if funds is None:
    id = insert(uid=uid, amount=amount, type=type)
  else:
    id = funds.id
    update(uid=uid, amount=amount, type=type)
  return insert_operation(funds=id, amount=amount, comment=comment)

def update_available(uid: int, amount: float, type: int = FUNDS_STOCK) -> int:
  stmt = sql_update(FundsTable) \
   .where(FundsTable.type == type) \
   .where(FundsTable.uid == uid) \
  .values(available=func.coalesce(FundsTable.available, 0) + amount, updated=func.now())
  return dbEngine.update_stmt(stmt)

