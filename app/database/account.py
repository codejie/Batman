from app.database import dbEngine, TableBase, Column, Integer, String, DateTime, func, sql_insert

class AccountTable(TableBase):
  __tablename__ = 'sys_account'

  id = Column(Integer, primary_key=True, autoincrement=True)
  account = Column(String, max=16, nullable=False)
  passwd = Column(String, max=64, nullable=False)
  name = Column(String, max=16, nullable=False)
  avatar = Column(String, nullable=True)
  comment = Column(String, nullable=True)
  updated = Column(DateTime(), server_default=func.now(), onupdate=func.current_timestamp())

def insert(account: str, passwd: str, name: str, avatar: str = None, comment: str = None) -> bool:
  stmt = sql_insert(AccountTable).values(
    account=account,
    passwd=passwd,
    name=name,
    avatar=avatar,
    comment=comment
  )
  return dbEngine.insert(stmt)
