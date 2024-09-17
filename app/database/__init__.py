"""
SQLAlchemy数据访问引擎
"""

from sqlalchemy import create_engine, Engine, case
from sqlalchemy import insert as sql_insert, select as sql_select, delete as sql_delete, update as sql_update, and_, or_
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Session, Bundle

from app.exception import AppException

DATABASE_URL: str = 'sqlite:///./app/db/batman.db'

class TableBase(DeclarativeBase):
    pass

class DBEngine:
    def __init__(self) -> None:
        self.engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False}) # .execution_options(isolation_level="AUTOCOMMIT")
    
    def start(self) -> bool:
        TableBase.metadata.create_all(self.engine)
        # self.insert(sql_insert(Version).values(version='0.2'))

    def shutdown(self) -> None:
        pass

    def get_engine(self):
        return self.engine

    def insert(self, stmt: object) -> bool:
        try:
            with Session(self.engine) as session:
                result = session.execute(stmt)
                session.commit()
                # if result.returns_rows:
                return result.inserted_primary_key[0]
                # else:
                #     return result.lastrowid
        except Exception as e:
            raise AppException(e)
        
    def select(self, stmt: object) -> list[any]:
        try:
            with Session(self.engine) as session:
                ret = []
                for r in session.scalars(stmt):
                    # print(f'=========select() - {r}')
                    ret.append(r)
                return ret
        except Exception as e:
            raise AppException(e)
        
    def select_one(self, stmt: object) -> any:
        try:
            with Session(self.engine) as session:
                ret = session.scalar(stmt)
                return ret
        except Exception as e:
            raise AppException(e)
    
    def select_with_execute(self, stmt: object) -> list[any]:
        try:
            with Session(self.engine) as session:
                ret = []
                for r in session.execute(stmt):
                    ret.append(r)
                return ret
        except Exception as e:
            raise AppException(e)
                
    def delete(self, stmt: object) -> int:
        try:
            with Session(self.engine) as session:
                result = session.execute(stmt)
                session.commit()
                return result.rowcount
        except Exception as e:
            raise AppException(e)
        
    def update(self, stmt: object) -> int:
        try:
            with Session(self.engine) as session:
                result = session.execute(stmt)
                session.commit()
                return result.rowcount
        except Exception as e:
            raise AppException(e)
                
dbEngine = DBEngine()