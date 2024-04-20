
from enum import Enum
from datetime import datetime, timedelta

from app import logger
from app.dbengine import engine, text

TABLE_FATCH_DATA_RECORD = 'sys_fetch_data_record'

class DataItem(Enum):
    STOCK_LIST = 1
    STOCK_DAILY_HISTORY = 2
    STOCK_DAILY_HSGT = 3
    STOCK_DAILY_MARGIN = 4

def select_item_latest(item: DataItem, code: str = None) -> dict | None:
    data = {
        'item': item.value
    }
    stmt = None

    if code:
        data['code'] = code
        stmt = text(f'SELECT end FROM {TABLE_FATCH_DATA_RECORD} WHERE item=:item AND code=:code ORDER BY updated DESC LIMIT 1')
    else:
        stmt = text(f'SELECT end FROM {TABLE_FATCH_DATA_RECORD} WHERE item=:item ORDER BY updated DESC LIMIT 1')

    with engine.connect() as conn:
        results = conn.execute(stmt, data)
        if results:
            result = results.first()
            if result:
                return result._asdict()
    return None

def insert_item_latest(item: DataItem, latest: str, code: str = None) -> dict | None:
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