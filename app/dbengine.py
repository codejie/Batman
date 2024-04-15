"""
SQLAlchemy数据访问引擎
"""

from sqlalchemy import create_engine, Engine, Column, Integer, String, DateTime, insert, select, delete
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.sql import func, text

DATABASE_URL = 'sqlite:///./app/db/batman.db'

class Base(DeclarativeBase):
    pass

class Version(Base):
    __tablename__ = 'system'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String)
    updated = Column(DateTime(timezone=True), server_default=func.now())

class TaskInstance(Base):
    __tablename__ = 'sys_task_instance'

    id = Column(String, primary_key=True)
    updated = Column(DateTime(timezone=True), server_default=func.now())

class DataUpdatedRecord(Base):
    __tablename__ = 'sys_data_updated_record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(Integer, nullable=False)
    start = Column(String, nullable=False)
    end = Column(String, nullable=False)
    result = Column(Integer, nullable=False)
    arg1 = Column(Integer, nullable=True)
    arg2 = Column(String, nullable=True)
    updated = Column(DateTime(timezone=True), server_default=func.now())

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False}) # .execution_options(isolation_level="AUTOCOMMIT")

def initDb(engine: Engine) -> bool:
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Version(version='0.1'))
        session.commit()

    return True

def shutdownDb(engine: Engine) -> None:
    pass
