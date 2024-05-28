"""
SQLAlchemy数据访问引擎
"""

from sqlalchemy import create_engine, Engine, Column, Integer, String, DateTime
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.sql import func

from app.exception import AppDataException

DATABASE_URL: str = 'sqlite:///./app/db/batman.db'
SYSTEM_VERSION: str = '0.2'

def DefaultNow():
    return func.now()

class TableBase(DeclarativeBase):
    pass

class Version(TableBase):
    __tablename__ = 'sys_infos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String)
    updated = Column(DateTime(timezone=True), server_default=DefaultNow())

class DBEngine:
    def __init__(self) -> None:
        self.engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False}) # .execution_options(isolation_level="AUTOCOMMIT")
    
    def start(self) -> bool:
        TableBase.metadata.create_all(self.engine)
        self.insert(Version(version=SYSTEM_VERSION))

    def shutdown(self) -> None:
        pass

    def insert(self, stmt: object) -> bool:
        try:
            with Session(self.engine) as session:
                session.add(stmt)
                session.commit()
                return True
        except Exception as e:
            raise AppDataException(e)
        
    def select(self, stmt: object) -> any:
        try:
            with Session(self.engine) as session:
                ret = session.scalars(stmt)
                return ret
        except Exception as e:
            raise AppDataException(e)

    def delete(self, stmt: object) -> int:
        try:
            with Session(self.engine) as session:
                result = session.execute(stmt)
                session.commit()
                return result.rowcount
        except Exception as e:
            raise AppDataException(e)
        
    def update(self, stmt: object) -> int:
        try:
            with Session(self.engine) as session:
                result = session.execute(stmt)
                session.commit()
                return result.rowcount
        except Exception as e:
            raise AppDataException(e)
        
dbEngine = DBEngine()