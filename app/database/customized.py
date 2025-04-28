
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, func, update, select as sql_select
from app.database import TableBase
from app.database import dbEngine
from app.database.data import define as Data

class CustomizedRecordTable(TableBase):
  __tablename__ = 'user_customized_record'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
  uid = Column(Integer, nullable=False, default=99)
  type = Column(Integer, nullable=False)
  code = Column(String, nullable=False)
  comment = Column(String, nullable=True)
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

class CustomizedRecord:
  id: int
  # uid: int
  type: int
  code: str
  name: str
  comment: str
  updated: datetime

def insert(uid:int, code: str, type: int = 1, comment: str = None) -> int:
  return dbEngine.insert_instance(CustomizedRecordTable(uid=uid, type=type, code=code, comment=comment))

def select(uid: int, type: int = None, code: str = None) -> list[CustomizedRecordTable]:
  stmt = sql_select(CustomizedRecordTable).where(CustomizedRecordTable.uid == uid)
  if type:
    stmt = stmt.where(CustomizedRecordTable.type == type)
  if code: 
    stmt = stmt.where(CustomizedRecordTable.code == code)
  return dbEngine.select_stmt(stmt)

def delete(uid: int, id: int) -> int:
  stmt = delete(CustomizedRecordTable).where(CustomizedRecordTable.uid == uid).where(CustomizedRecordTable.id == id)
  return dbEngine.delete(stmt=stmt)

def update_comment(id: int, comment: str = None) -> int:
  stmt = update(CustomizedRecordTable).values(comment=comment, updted=func.now()).where(CustomizedRecordTable.id == id)
  return dbEngine.update(stmt=stmt)

def records(uid: int, type: int = None, code: str = None) -> list[CustomizedRecord]:
  stmt = select(CustomizedRecordTable, Data.InfoTable.name.label('name')).where(CustomizedRecordTable.uid == uid)
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
      comment=row[0].comment,
      updated=row[0].updated
    ))
  return ret
