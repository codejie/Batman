
from sqlalchemy import Column, Integer, String, inspect
from app.database import dbEngine, TableBase

DATATYPE_HISTORY: int = 1

def create_dynamic_table_class(code: str, datatype: int):
  class DynamicTable(TableBase):
    __tablename__ = f"stock_{datatype}_{code}"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Integer)
  
  return DynamicTable

def fetch_table(code: str, datatype: int = DATATYPE_HISTORY) -> TableBase:
  table = create_dynamic_table_class(code, datatype)
  exists = inspect(dbEngine.engine).has_table(table.__tablename__)
  if not exists:
    table.__table__.create(dbEngine.engine)
  return table
