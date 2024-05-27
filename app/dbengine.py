"""
SQLAlchemy数据访问引擎
"""

from sqlalchemy import create_engine, Engine, Column, Integer, String, Float, BigInteger, DateTime, insert, select, delete
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

class SystemFetchDataRecord(Base):
    __tablename__ = 'sys_fetch_data_record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(Integer, nullable=False)
    code = Column(String, nullable=True)
    latest = Column(String, nullable=False)
    updated = Column(DateTime(timezone=True), server_default=func.now())

class ViewDataRecord(Base):
    __tablename__ = 'view_data_record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(Integer, nullable=False)
    latest = Column(String, nullable=False)
    updated = Column(DateTime(timezone=True), server_default=func.now())    


class ViewStockDailyHistory(Base):
    __tablename__ = 'view_stock_daily'

    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volumn = Column(BigInteger)
    turnover = Column(Float)
    volatility = Column(Float)
    percentage = Column(Float)
    amount = Column(Float)
    rate = Column(Float)
    

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False}) # .execution_options(isolation_level="AUTOCOMMIT")

def initDb(engine: Engine) -> bool:
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(Version(version='0.1'))
        session.commit()

    return True

def shutdownDb(engine: Engine) -> None:
    pass
