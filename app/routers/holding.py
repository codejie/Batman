from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from app.exception import AppException

DATABASE_URL: str = 'sqlite:///./app/db/batman.db'

class TableBase(DeclarativeBase):
  pass

class DBEngine:
  def __init__(self) -> None:
    self.engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

  def start(self) -> bool:
    TableBase.metadata.create_all(self.engine)
    return True
  
  def shutdown(self) -> None:
      pass
  
  def stmt_insert(self, stmt: object) -> Optional[int]:
    try:
      with Session(self.engine) as session:
        result = session.execute(stmt)
        session.commit()
        # session.close()
        return result.inserted_primary_key[0]
    except Exception as e:
      raise AppException(e)

  def instance_insert(self, instance: TableBase) -> Optional[int]:
    try:
      with Session(self.engine) as session:
        session.add(instance)
        session.commit()
        return instance.id
    except Exception as e:
      raise AppException(e)