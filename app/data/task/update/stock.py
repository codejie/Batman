"""
Stock data init
"""
from datetime import datetime

from app.exception import AppDataException
from app.database import dbEngine, text
from app.database.tables import TableName
from app.data.local_db import stock as local
from app.data.task.update import records

HISTORY_START =  datetime(year=2023, month=1, day=1, hour=0, minute=0, second=0)

def init_check() -> None:
    try:
        # if not exist_list_table():
        if_exists = 'replace'
        start = HISTORY_START
        end = datetime.now()

        fetch_list(start=start, end=end, if_exists=if_exists)
            # symbols = get_list()

            # if_exists = 'replace'
            # fetch_daily_history(start=)
            # fetch_hsgt()
            # fetch_margin()            
    except Exception as e:
        raise AppDataException(e)

def exist_list_table() -> bool:
    stmt = text(f'SELECT count(*) FROM sqlite_master WHERE name="{TableName.Stock_A_List}"')
    result = dbEngine.select_one(stmt)
    return result == 1

def fetch_list(start: datetime, end: datetime, if_exists: str) -> None:
    # local.fetch_a_stock(if_exists=if_exists)
    records.upsert(records.Item.STOCK_LIST, end)
    ret = records.get_latest(records.Item.STOCK_LIST)
    print(ret)
