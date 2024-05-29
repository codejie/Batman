"""
数据更新记录函数
"""
from datetime import datetime
from enum import Enum
from app.database.tables import TableBase, Column, Integer, String, DateTime, DefaultNow
from app.database import dbEngine, insert as db_insert, select as db_select, update as db_update

class ItemUpdatedRecordTable(TableBase):
    __tablename__ = 'sys_item_updated_record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(Integer)
    code = Column(String, nullable=True)
    latest = Column(DateTime)
    updated = Column(DateTime(timezone=True), server_default=DefaultNow())

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

def upsert(item: Item, latest: datetime, code: str = None) -> bool:
    stmt = db_insert(ItemUpdatedRecordTable).values(
        item=item.value,
        latest=latest,
        code=code
    )
    stmt.on_conflict_do_update(
        index_elements=[ItemUpdatedRecordTable.item, ItemUpdatedRecordTable.code],
        set_=dict(latest=stmt.excluded.latest)
        )
    return dbEngine.insert(stmt=stmt)

def update(item: Item, latest: datetime, code: str = None) -> int:
    stmt = db_update(ItemUpdatedRecordTable).values(latest=latest)
    if code:
        stmt = stmt.where(item==item, code=code)
    else:
        stmt = stmt.where(item==item)
    return dbEngine.update(stmt=stmt)

def get_latest(item: Item, code: str = None) -> datetime | None:
    stmt = db_select(ItemUpdatedRecordTable).order_by(ItemUpdatedRecordTable.updated.desc())
    if code:
        stmt = stmt.where(item==item, code=code)
    else:
        stmt = stmt.where(item==item)
    
    result = dbEngine.select_one(stmt)
    if result:
        return result.latest
    return None
