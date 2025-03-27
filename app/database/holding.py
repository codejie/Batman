import datetime
from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Index, Integer, String, DateTime, case, select, update
from sqlalchemy.sql import func
from app.database import dbEngine, TableBase
from app.database import info as Info

HOLDING_FLAG_ACTIVE: int = 0
HOLDING_FLAG_REMOVED: int = 1
OPERATION_ACTION_BUY: int = 0
OPERATION_ACTION_SELL: int = 1

class HoldingTable(TableBase):
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

class HoldingOperationTable(TableBase):
  __tablename__ = 'user_holding_operation_table'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  holding = Column(Integer, ForeignKey(HoldingTable.id), nullable=False)
  action = Column(Integer, nullable=False)
  quantity = Column(Integer, nullable=False)
  price = Column(Float, nullable=False)
  expense = Column(Float, nullable=False)
  comment = Column(String, nullable=True)
  created = Column(DateTime(timezone=True), server_default=func.now())

class UserHoldingRecord(BaseModel):
  id: int
  type: int
  code: str
  name: str
  flag: int
  created: datetime.datetime
  updated: datetime.datetime
  quantity: int
  expense: float

def insert_holding(uid: int, type: int, code: str) -> int:
  return dbEngine.insert_instance(HoldingTable(uid=uid, type=type, code=code))

def insert_operation(id: int, action: int, quantity: int, price: float, expense: float, comment: str = None) -> int:
  return dbEngine.insert_instance(HoldingOperationTable(holding=id, action=action, quantity=quantity, price=price, expense=expense, comment=comment))

def select_holding(uid: int, type: int = None, code: str = None, flag: int = None) -> list[HoldingTable]:
  stmt = select(HoldingTable).where(HoldingTable.uid == uid)
  if type:
    stmt = stmt.where(HoldingTable.type == type)
  if code: 
    stmt = stmt.where(HoldingTable.code == code)
  if flag:
    stmt = stmt.where(HoldingTable.flag == flag)
  return dbEngine.select_stmt(stmt)

def select_operation(uid: int, holding: int = None) -> list[HoldingOperationTable]:
  stmt = select(HoldingOperationTable).order_by(HoldingOperationTable.created.desc())
  if holding:
    stmt = stmt.where(HoldingOperationTable.holding == holding)
  return dbEngine.select_stmt(stmt)

def update_holding_flag(uid: int, id: int, flag: int) -> int:
  return dbEngine.update_stmt(update(HoldingTable).where(HoldingTable.id == id and HoldingTable.uid == uid).values([
    {'flag': flag, 'updated': func.now()}
  ]))

"""
Combination API
"""
def create(uid: int, type: int, code: str, action: int, quantity: int, price: float, expense: float, comment: str = None) -> int:
  records = dbEngine.select_stmt(select(HoldingTable)
                                 .where(HoldingTable.uid == uid)
                                 .where(HoldingTable.type == type)
                                 .where(HoldingTable.code == code))
  id = -1
  if len(records) == 0:
    id = dbEngine.insert_instance(HoldingTable(uid=uid, type=type, code=code))
  else:
    id = records[0].id
    if records[0].flag == HOLDING_FLAG_REMOVED:
      dbEngine.update_stmt(update(HoldingTable).where(HoldingTable.id == id).values([
        {'flag': HOLDING_FLAG_ACTIVE, 'updated': func.now()}
      ]))
  dbEngine.insert_instance(HoldingOperationTable(holding=id, action=action, quantity=quantity, price=price, expense=expense, comment=comment))
  return id

def records(uid: int, id: int = None, type: int = None, code: str = None, flag: int = None) -> list[UserHoldingRecord]:
  stmt = select(HoldingTable,
                Info.InfoTable.name.label('name'),
                func.coalesce(
                  func.sum(case((HoldingOperationTable.action == OPERATION_ACTION_BUY, HoldingOperationTable.quantity), else_=-HoldingOperationTable.quantity)),
                  0).label('quantity'),
                func.coalesce(
                  func.sum(case((HoldingOperationTable.action == OPERATION_ACTION_BUY, -HoldingOperationTable.expense), else_=HoldingOperationTable.expense)),
                  0.0).label('expense')
              ).select_from(HoldingTable
              ).join(Info.InfoTable, Info.InfoTable.code == HoldingTable.code and Info.InfoTable.type == HoldingTable.type, isouter=True
              ).join(HoldingOperationTable, HoldingOperationTable.holding == HoldingTable.id, isouter=True
              ).filter(HoldingTable.uid == uid
              ).group_by(HoldingTable.id
              ).order_by(HoldingTable.updated.desc())
  if id:
    stmt = stmt.where(HoldingTable.id == id)
  if type:
    stmt = stmt.where(HoldingTable.type == type)
  if code:
    stmt = stmt.where(HoldingTable.code == code)
  if flag:
    stmt = stmt.where(HoldingTable.flag == flag)
  
  # print(str(stmt))
  results = dbEngine.select_stmt(stmt)
  
  ret: list[UserHoldingRecord] = []
  for r in results:
    ret.append(UserHoldingRecord(
      id=r[0].id,
      type=r[0].type,
      code=r[0].code,
      name=r[1],
      flag=r[0].flag,
      created=r[0].created,
      updated=r[0].updated,
      quantity=r[2],
      expense=r[3]
    ))
  return ret
