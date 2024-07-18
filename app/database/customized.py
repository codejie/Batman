
from app.database import TableBase, Column, Integer, String, DateTime, func
from app.database import dbEngine, sql_insert, sql_delete, sql_update, and_

class CustomizedRecordTable(TableBase):
  __tablename__ = 'user_customized_record'

  id = Column(Integer, autoincrement=True, primary_key=True)
  uid = Column(Integer, nullable=False, default=99)
  type = Column(Integer, default=1)
  code = Column(String, nullable=False)
  comment = Column(String, nullable=True)
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

def insert(code: str, uid: int = 99, type: int = 1, comment: str = None) -> bool:
  stmt = sql_insert(CustomizedRecordTable).values(
    uid=uid,
    type=type,
    code=code,
    comment=comment
  )
  return dbEngine.insert(stmt=stmt)

def delete(code: str, uid: int = 99, type: int = 1) -> int:
  stmt = sql_delete(CustomizedRecordTable).where(and_(
    CustomizedRecordTable.uid == uid,
    CustomizedRecordTable.code == code,
    CustomizedRecordTable.type == type))
  return dbEngine.delete(stmt=stmt)

def update_comment(id: int, comment: str = None) -> int:
  stmt = sql_update(CustomizedRecordTable).values(comment=comment).where(CustomizedRecordTable.id == id)
  return dbEngine.update(stmt=stmt)
