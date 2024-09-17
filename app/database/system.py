from app.database import dbEngine, TableBase, Column, Integer, String, DateTime, func, sql_insert

SYSTEM_VERSION: str = '0.2'

class SystemInfosTable(TableBase):
  __tablename__ = 'sys_infos'
  
  id = Column(Integer, primary_key=True, autoincrement=True)
  version = Column(String)
  updated = Column(DateTime(timezone=True), server_default=func.now())

def insert_info() -> int:
    return dbEngine.insert(sql_insert(SystemInfosTable).values(version='0.2'))
