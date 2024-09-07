"""
数据更新记录函数
"""
from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy.sql import and_
from app.database import TableBase, Column, Integer, String, DateTime, func
from app.database import dbEngine, sql_insert, sql_select, sql_update

HISTORY_START =  datetime(year=2023, month=1, day=1, hour=0, minute=0, second=0)

class ItemUpdatedRecordTable(TableBase):
    __tablename__ = 'sys_item_updated_record'

 
    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(Integer)
    code = Column(String, nullable=True)
    latest = Column(DateTime)
    updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())

class Item(Enum):
    STOCK_LIST = 1
    STOCK_DAILY_HISTORY = 2
    STOCK_DAILY_HSGT = 3
    STOCK_DAILY_MARGIN = 4

    INDEX_LIST = 101
    INDEX_DAILY_HISTORY = 102

def insert(item: Item, latest: datetime, code: str = None) -> bool:
    stmt = sql_insert(ItemUpdatedRecordTable).values(
        item=item.value,
        latest=latest,
        code=code
    )
    ret = dbEngine.insert(stmt=stmt)
    return ret

# def upsert(item: Item, latest: datetime, code: str = None) -> bool:
#     stmt = sql_insert(ItemUpdatedRecordTable).values(
#         item=item.value,
#         latest=latest,
#         code=code
#     )
#     stmt = stmt.on_conflict_do_update(
#         index_elements=['item', 'code'],
#         set_=dict(latest=latest)
#         )
#     return dbEngine.insert(stmt=stmt)

def update(item: Item, latest: datetime, code: str = None) -> int:
    stmt = sql_update(ItemUpdatedRecordTable).values(latest=latest)
    if code:
        stmt = stmt.where(and_(ItemUpdatedRecordTable.item == item.value, ItemUpdatedRecordTable.code == code))
    else:
        stmt = stmt.where(ItemUpdatedRecordTable.item == item.value)
    return dbEngine.update(stmt=stmt)

def get_latest(item: Item, code: str = None) -> datetime | None:
    stmt = sql_select(ItemUpdatedRecordTable).order_by(ItemUpdatedRecordTable.updated.desc())
    if code:
        stmt = stmt.where(and_(ItemUpdatedRecordTable.item == item.value, ItemUpdatedRecordTable.code == code))
    else:
        stmt = stmt.where(ItemUpdatedRecordTable.item == item.value)  
    result = dbEngine.select_one(stmt)
    if result:
        return result.latest
    return None

def set_latest(item: Item, latest: datetime, code: str = None, is_update: bool = False) -> int:
    if is_update:
        update(item, latest, code)
    else:
        insert(item, latest, code)

def get_start_end(item: Item, code: str = None) -> tuple:
    start = HISTORY_START
    latest = get_latest(item, code)
    is_update = False
    if latest:
        start = latest + timedelta(days=1)
        is_update = True

    return (start, datetime.now(), is_update)