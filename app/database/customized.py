
from app.database import TableBase, Column, Integer, String, DateTime, func
from app.database import dbEngine, Bundle, sql_insert, sql_delete, sql_update, sql_select, and_
from app.database import stock
from app.database.tables import StockAListTable

class CustomizedRecordTable(TableBase):
  __tablename__ = 'user_customized_record'

  id = Column(Integer, autoincrement=True, primary_key=True)
  uid = Column(Integer, nullable=False, default=99)
  type = Column(Integer, default=1)
  code = Column(String, nullable=False)
  comment = Column(String, nullable=True)
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

def insert(uid:int, code: str, type: int = 1, comment: str = None) -> bool:
  stmt = sql_insert(CustomizedRecordTable).values(
    uid=uid,
    type=type,
    code=code,
    comment=comment
  )
  return dbEngine.insert(stmt=stmt)

def find(uid: int, code: str, type: int = 1) -> bool:
  stmt = sql_select(func.count(CustomizedRecordTable.code)).where(CustomizedRecordTable.uid==uid).where(and_(CustomizedRecordTable.code==code,CustomizedRecordTable.type==type))
  ret = dbEngine.select_one(stmt=stmt)
  return ret > 0

def delete(id: int) -> int:
  stmt = sql_delete(CustomizedRecordTable).where(CustomizedRecordTable.id == id)
  return dbEngine.delete(stmt=stmt)

def update_comment(id: int, comment: str = None) -> int:
  stmt = sql_update(CustomizedRecordTable).values(comment=comment).where(CustomizedRecordTable.id == id)
  return dbEngine.update(stmt=stmt)

def get_list(uid: int, type: int = 1) -> list:
  stmt = sql_select(CustomizedRecordTable, StockAListTable.name).join(
      StockAListTable, CustomizedRecordTable.code == StockAListTable.code
    ).filter(
      CustomizedRecordTable.uid == uid
    )
  # stmt = sql_select(StockAListTable.name, CustomizedRecordTable).select_from(CustomizedRecordTable).join(
  #     StockAListTable, CustomizedRecordTable.code == StockAListTable.code
  #   ).filter(
  #     CustomizedRecordTable.uid == uid
  #   )  
  results = dbEngine.select_with_execute(stmt=stmt)

  ret = []
  for row in results:
    ret.append({
      'id': row[0].id,
      'type': row[0].type,
      'code': row[0].code,
      'name': row[1],
      'comment': row[0].comment,
      'updated': row[0].updated
    })
  return ret
