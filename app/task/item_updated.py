
from enum import Enum
from datetime import datetime, timedelta

from app import logger
from app.dbengine import engine, text
from app import utils

HISTORY_START =  datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0)

TABLE_FATCH_DATA_RECORD = 'sys_fetch_data_record'

class DataItem(Enum):
    STOCK_LIST = 1
    STOCK_DAILY_HISTORY = 2
    STOCK_DAILY_HSGT = 3
    STOCK_DAILY_MARGIN = 4

def select_item_latest(item: DataItem, code: str = None) -> str | None:
    data = {
        'item': item.value
    }
    stmt = None

    if code:
        data['code'] = code
        stmt = text(f'SELECT latest FROM {TABLE_FATCH_DATA_RECORD} WHERE item=:item AND code=:code ORDER BY updated DESC LIMIT 1')
    else:
        stmt = text(f'SELECT latest FROM {TABLE_FATCH_DATA_RECORD} WHERE item=:item ORDER BY updated DESC LIMIT 1')

    with engine.connect() as conn:
        results = conn.execute(stmt, data)
        if results:
            result = results.first()
            if result:
                return result.latest #  ._asdict()
    return None

def insert_item_latest(item: DataItem, latest: str, code: str = None) -> int:
    data = {
        'item': item.value,
        'latest': latest,
        'code': code
    }

    stmt = text(f'INSERT INTO {TABLE_FATCH_DATA_RECORD}(item, latest, code) VALUES(:item, :latest, :code)')
    with engine.connect() as conn:
        ret = conn.execute(stmt, data)
        conn.commit()
        return ret.rowcount
    
def update_item_latest(item: DataItem, latest: str, code: str = None) -> int:
    data = {
        'item': item.value,
        'latest': latest,
        'code': code,
        'updated': datetime.now()
    }

    stmt = text(f'UPDATE {TABLE_FATCH_DATA_RECORD} SET latest=:latest, updated=:updated WHERE item=:item{" AND code=:code" if code else ""}')
    with engine.connect() as conn:
        ret = conn.execute(stmt, data)
        conn.commit()
        return ret.rowcount
    
    
def get_item_start_end(item: DataItem, code: str = None) -> tuple:
    start = HISTORY_START
    latest = select_item_latest(item, code)
    insert = True
    if latest:
        latest = utils.string2Date2(latest)
        start =  latest + timedelta(days=1)
        insert = False
    end = datetime.now().date()
    if start < end:
        return (utils.date2String2(start), utils.date2String2(end), insert)
    else:
        return (None, None, insert)


def set_item_latest(item: DataItem, latest: str, code: str = None, insert: bool = False) -> int:
    if insert:
        return insert_item_latest(item, latest, code)
    else:
        return update_item_latest(item, latest, code)