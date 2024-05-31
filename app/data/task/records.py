"""
数据更新记录函数
"""
from datetime import datetime, timedelta
from enum import Enum
from app.database.tables import TableBase, Column, Integer, String, DateTime, func
from app.database import dbEngine, insert as db_insert, select as db_select, update as db_update

HISTORY_START =  datetime(year=2024, month=1, day=1, hour=0, minute=0, second=0)

class ItemUpdatedRecordTable(TableBase):
    __tablename__ = 'sys_item_updated_record'

 
    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(Integer)
    code = Column(String, nullable=True)
    latest = Column(DateTime)
    updated = Column(DateTime(timezone=True), server_default=func.now())

class Item(Enum):
    STOCK_LIST = 1
    STOCK_DAILY_HISTORY = 2
    STOCK_DAILY_HSGT = 3
    STOCK_DAILY_MARGIN = 4

def insert(item: Item, latest: datetime, code: str = None) -> bool:
    stmt = db_insert(ItemUpdatedRecordTable).values(
        item=item.value,
        latest=latest,
        code=code
    )
    ret = dbEngine.insert(stmt=stmt)
    return ret

# def upsert(item: Item, latest: datetime, code: str = None) -> bool:
#     stmt = db_insert(ItemUpdatedRecordTable).values(
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
    stmt = db_update(ItemUpdatedRecordTable).values(latest=latest)
    if code:
        stmt = stmt.where(item==item, code==code)
    else:
        stmt = stmt.where(item==item)
    return dbEngine.update(stmt=stmt)

def get_latest(item: Item, code: str = None) -> datetime | None:
    stmt = db_select(ItemUpdatedRecordTable).order_by(ItemUpdatedRecordTable.updated.desc())
    if code:
        stmt = stmt.where(item==item, code==code)
    else:
        stmt = stmt.where(item==item)
    
    result = dbEngine.select_one(stmt)
    if result:
        return result.latest
    return None

def set_latest(item: Item, latest: datetime, code: str = None, is_update: bool = False) -> int:
    if is_update:
        update(Item.STOCK_DAILY_HISTORY, latest, code)
    else:
        insert(Item.STOCK_DAILY_HISTORY, latest, code)

def get_start_end(item: Item, code: str = None) -> tuple:
    start = HISTORY_START
    latest = get_latest(item, code)
    is_update = False
    if latest:
        start = latest + timedelta(days=1)
        is_update = True

    return (start, datetime.now(), is_update)