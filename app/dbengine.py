"""
SQLAlchemy数据访问引擎
"""

from sqlalchemy import create_engine, Engine, Column, Integer, String, DateTime, insert, select, delete
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.sql import func

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
    # file = Column(String)
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
