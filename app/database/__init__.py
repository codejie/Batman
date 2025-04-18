from typing import Optional
from sqlalchemy import create_engine, inspect, text
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
  
  def check_table_exist(self, table: str) -> bool:
    inspector = inspect(self.engine)
    return inspector.has_table(table)

  def insert_stmt(self, stmt: object) ->int:
    try:
      with Session(self.engine) as session:
        result = session.execute(stmt)
        session.commit()
        return result.inserted_primary_key[0] if result.inserted_primary_key else 0
    except Exception as e:
      raise AppException(e)

  def insert_instance(self, instance: TableBase) -> int:
    try:
      with Session(self.engine) as session:
        session.add(instance)
        session.commit()
        return instance.id if instance.id else 0
    except Exception as e:
      raise AppException(e)
    
  def select_stmt(self, stmt: object) -> list[any]:
    try:
        with Session(self.engine) as session:
            ret = []
            for r in session.execute(stmt):
                ret.append(r)
            return ret
    except Exception as e:
        raise AppException(e)
  
  def select_scalars(self, stmt: object) -> list[any]:
    try:
      with Session(self.engine) as session:
        ret = []
        for r in session.scalars(stmt):
          ret.append(r)
        return ret
    except Exception as e:
      raise AppException(e)
    
  def select_scalar(self, stmt: object) -> any:
    try:
      with Session(self.engine) as session:
        return session.scalar(stmt)
    except Exception as e:
      raise AppException(e)
    
  def delete_stmt(self, stmt: object) -> int:
    try:
      with Session(self.engine) as session:
        result = session.execute(stmt)
        session.commit()
        return result.rowcount
    except Exception as e:
      raise AppException(e)
    
  def update_stmt(self, stmt: object) -> int:
    try:
      with Session(self.engine) as session:
        result = session.execute(stmt)
        session.commit()
        return result.rowcount
    except Exception as e:
      raise AppException(e)
    
  def bulk_insert_data(self, table, data: list[dict]) -> None:
    try:
      with Session(self.engine) as session:
        # session.execute(text(f"TRUNCATE TABLE {table.__tablename__}"))
        # session.query(table).delete()
        # session.commit()
        session.bulk_insert_mappings(table, data)
        session.commit()
    except Exception as e:
      raise AppException(e)
    
dbEngine = DBEngine()