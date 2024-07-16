from app.database import dbEngine
from app.database.tables import TableBase, Column, Integer, String, DateTime, func

class CustomizedRecordTable(TableBase):
  ___tablename__ = 'user_customized_record'

  id = Column(Integer, autoincrement=True, primary_key=True)
  uid = Column(Integer, nullable=False, default=99)
  type = Column(Integer, default=1)
  code = Column(String, len=6, nullable=False)
  comment = Column(String, nullable=True)
  updated = Column(DateTime(timezone=True), server_default=func.now())
