import datetime
import json
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, Session

from app.exception import AppException

DATABASE_URL: str = 'sqlite:///./app/db/batman.db'

def convert_datetime_to_serializable(value): 
  """Convert non-serializable objects to JSON-serializable formats."""
  if isinstance(value, datetime.datetime):
      return value.strftime("%Y-%m-%d %H:%M:%S.%f")  # Format as 2025-04-15 09:15:24.855000
  return value

def parse_datetime_from_serializable(value, is_datetime):
    """Convert datetime string in '2025-04-15 09:15:24.855000' format to datetime object."""
    if value is None:
        return None
    if is_datetime:
      return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    return value

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

  def trunc_table(self, table) -> None:
    try:
      with Session(self.engine) as session:
        session.query(table).delete()
        session.commit()
    except Exception as e:
      raise AppException(e)
    
  def export_json(self, table: TableBase, file_name: str) -> int:
    with Session(self.engine) as session:
      records = session.query(table).all()
      columns = table.__table__.columns.keys()
      records_list = [
        {column: convert_datetime_to_serializable(getattr(record, column)) for column in columns}
        for record in records
      ]
      with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(records_list, f, indent=2, ensure_ascii=False)

      return len(records_list)

  def import_json(self, table: TableBase, file_name: str, is_replace: bool = True) -> int:
    if is_replace:
      self.trunc_table(table)

    with open(file_name, 'r', encoding='utf-8') as f:
      data = json.load(f)

      datetime_columns = [column.name for column in table.__table__.columns if column.type.python_type == datetime.datetime]

      # instances = []
      for record in data:
        instance = table(**{k: parse_datetime_from_serializable(v, (k in datetime_columns)) for k, v in record.items()})
        self.insert_instance(instance)

      # return self.bulk_insert_data(model, instances)
    return len(data)
  
dbEngine = DBEngine()