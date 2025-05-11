
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, Index, Integer, String, func, update, select as sql_select, delete as sql_delete
from app.database import TableBase
from app.database import dbEngine
from app.database.data import define as Data, is_item_exist
from app.database.holding import HOLDING_FLAG_ACTIVE, HoldingTable
from app.exception import AppException

class CustomizedRecordTable(TableBase):
  __tablename__ = 'user_customized_record'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
  uid = Column(Integer, nullable=False, default=99)
  type = Column(Integer, nullable=False)
  code = Column(String, nullable=False)
  target = Column(Float, nullable=True)
  order = Column(Integer, nullable=False, default=0)
  comment = Column(String, nullable=True)
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

  __table_args__ = (
    Index('idx_user_customized_record_type_code', 'type', 'code'),
  )

class CustomizedRecord(BaseModel):
  id: int
  # uid: int
  type: int
  code: str
  name: str
  target: Optional[float] = None
  order: int = 0
  comment: Optional[str] = None
  updated: datetime
  holding: Optional[int] = None

def insert(uid:int, code: str, type: int = 1, comment: str = None) -> int:
  stmt = sql_select(CustomizedRecordTable).where(CustomizedRecordTable.uid == uid).where(CustomizedRecordTable.type == type).where(CustomizedRecordTable.code == code)
  result = dbEngine.select_scalar(stmt)
  if result:
    return result.id
  exists = is_item_exist(type=type, code=code)
  if exists:
    return dbEngine.insert_instance(CustomizedRecordTable(uid=uid, type=type, code=code, comment=comment))
  else:
    raise AppException(f"Item not found: {type}, {code}")

def select(uid: int, type: int = None, code: str = None) -> list[CustomizedRecordTable]:
  stmt = sql_select(CustomizedRecordTable).where(CustomizedRecordTable.uid == uid)
  if type:
    stmt = stmt.where(CustomizedRecordTable.type == type)
  if code: 
    stmt = stmt.where(CustomizedRecordTable.code == code)
  return dbEngine.select_stmt(stmt)

def delete(uid: int, id: int) -> int:
  stmt = sql_delete(CustomizedRecordTable).where(CustomizedRecordTable.uid == uid).where(CustomizedRecordTable.id == id)
  return dbEngine.delete_stmt(stmt=stmt)

def update_comment(uid: int, id: int, comment: str = None) -> int:
  stmt = update(CustomizedRecordTable).values(comment=comment, updted=func.now()).where(CustomizedRecordTable.id == id).where(CustomizedRecordTable.uid == uid)
  return dbEngine.update_stmt(stmt=stmt)

def update_target(uid: int, id: int, target: float = None) -> int:
  stmt = update(CustomizedRecordTable).values(target=target, updated=func.now()).where(CustomizedRecordTable.id == id).where(CustomizedRecordTable.uid == uid)
  return dbEngine.update_stmt(stmt=stmt)

def update_order(uid: int, id: int, order: int = 0) -> int:
  stmt = update(CustomizedRecordTable).values(order=order, updated=func.now()).where(CustomizedRecordTable.id == id).where(CustomizedRecordTable.uid == uid)
  return dbEngine.update_stmt(stmt=stmt)

def records(uid: int, type: int = None, code: str = None) -> list[CustomizedRecord]:
  stmt = sql_select(CustomizedRecordTable, Data.InfoTable.name.label('name'), func.coalesce(HoldingTable.id, None).label('holding')
                    ).select_from(CustomizedRecordTable
                    ).join(Data.InfoTable, (Data.InfoTable.code == CustomizedRecordTable.code) & (Data.InfoTable.type == CustomizedRecordTable.type), isouter=False
                    ).join(HoldingTable, (HoldingTable.code == CustomizedRecordTable.code) & (HoldingTable.type == CustomizedRecordTable.type) & (HoldingTable.flag == HOLDING_FLAG_ACTIVE), isouter=True
                    ).where(CustomizedRecordTable.uid == uid)
  if type:
    stmt = stmt.where(CustomizedRecordTable.type == type)
  if code: 
    stmt = stmt.where(CustomizedRecordTable.code == code)
  ret: list[CustomizedRecord] = []
  results = dbEngine.select_stmt(stmt)
  for row in results:
    ret.append(CustomizedRecord(
      id=row[0].id,
      # uid=row[0].uid,
      type=row[0].type,
      code=row[0].code,
      name=row[1],
      target=row[0].target,
      order=row[0].order,
      holding=row[2],
      comment=row[0].comment,
      updated=row[0].updated
    ))
  return ret
