
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Index, Integer, String, func, update, select as sql_select, delete as sql_delete
from app.database import TableBase
from app.database import dbEngine
from app.database.data import define as Data
from app.database.holding import HOLDING_FLAG_ACTIVE, HoldingTable

class CustomizedRecordTable(TableBase):
  __tablename__ = 'user_customized_record'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
  uid = Column(Integer, nullable=False, default=99)
  type = Column(Integer, nullable=False)
  code = Column(String, nullable=False)
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
  comment: Optional[str] = None
  updated: datetime
  holding: Optional[int] = None

def insert(uid:int, code: str, type: int = 1, comment: str = None) -> int:
  stmt = sql_select(CustomizedRecordTable).where(CustomizedRecordTable.uid == uid).where(CustomizedRecordTable.type == type).where(CustomizedRecordTable.code == code)
  result = dbEngine.select_scalar(stmt)
  if result:
    return result.id
  return dbEngine.insert_instance(CustomizedRecordTable(uid=uid, type=type, code=code, comment=comment))

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

def update_comment(id: int, comment: str = None) -> int:
  stmt = update(CustomizedRecordTable).values(comment=comment, updted=func.now()).where(CustomizedRecordTable.id == id)
  return dbEngine.update_stmt(stmt=stmt)

def records(uid: int, type: int = None, code: str = None) -> list[CustomizedRecord]:
  stmt = sql_select(CustomizedRecordTable, Data.InfoTable.name.label('name'), func.coalesce(HoldingTable.id, None).label('holding')).select_from(CustomizedRecordTable
                    ).join(Data.InfoTable, Data.InfoTable.code == CustomizedRecordTable.code and Data.InfoTable.type == CustomizedRecordTable.type, isouter=True
                    ).join(HoldingTable, HoldingTable.code == CustomizedRecordTable.code and HoldingTable.type == CustomizedRecordTable.type and HoldingTable.flag == HOLDING_FLAG_ACTIVE, isouter=True
                    ).where(CustomizedRecordTable.uid == uid)
  if type:
    stmt = stmt.where(CustomizedRecordTable.type == type)
  if code: 
    stmt = stmt.where(CustomizedRecordTable.code == code)
  print(stmt)
  ret: list[CustomizedRecord] = []
  results = dbEngine.select_stmt(stmt)
  for row in results:
    ret.append(CustomizedRecord(
      id=row[0].id,
      # uid=row[0].uid,
      type=row[0].type,
      code=row[0].code,
      name=row[1],
      holding=row[2],
      comment=row[0].comment,
      updated=row[0].updated
    ))
  return ret
