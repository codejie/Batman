"""
数据任务
"""
from enum import Enum
from datetime import datetime, timedelta

from app import logger, utils
from app.dbengine import engine, text
from app.data.local_db import stock

TABLE_SYSTEM_DATA_UPDATED_RECORD = 'sys_data_updated_record'
HISTORY_START =  datetime(year=2022, month=1, day=1)

class DataItem(Enum):
    STOCK_LIST = 1
    STOCK_DAILY_HISTORY = 2
    STOCK_DAILY_HSGT = 3
    STOCK_DAILY_MARGIN = 4


    INDEX_LIST = 1000

def select_last_item(item: DataItem) -> dict | None:
    data = {
        'item': item.value,
        'result': 0
    }
    stmt = text(f'SELECT item, start, end, result, arg1, arg2 FROM {TABLE_SYSTEM_DATA_UPDATED_RECORD} WHERE item=:item AND result=:result ORDER BY updated DESC LIMIT 1')
    with engine.connect() as conn:
        results = conn.execute(stmt, data)
        if results:
            result = results.first()
            if result:
                return result._asdict()
    return None

def insert_last_item(item: DataItem, start: datetime, end: datetime, result: int, arg1: int = None, arg2: str = None) -> int:
    data = {
        'item': item.value,
        'start': start,
        'end': end,
        'result': result,
        'arg1': arg1,
        'arg2': arg2
    }

    stmt = text(f'INSERT INTO {TABLE_SYSTEM_DATA_UPDATED_RECORD}(item, start, end, result, arg1, arg2) VALUES(:item, :start, :end, :result, :arg1, :arg2)')
    with engine.connect() as conn:
        ret = conn.execute(stmt, data)
        conn.commit()
        return ret.rowcount


"""
System Data Check
"""
def system_daily_data_updated_check(**kwargs):
    logger.info('system_daily_data_updated_check() start.')
    # STOCK_LIST
    fetch_stock_list(**kwargs)
    # STOCK_DAILY_HISTORY
    fetch_stock_history(**kwargs)

    logger.info('system_daily_data_updated_check() end.')


"""
Stock List check
"""
def fetch_stock_list(**kwargs):
    logger.info('fetch_stock_list() start.')
    item = select_last_item(DataItem.STOCK_LIST)
    # print(item)
    try:
        if item is None:
            stock.fetch_a_stock(if_exists='replace')
        start = datetime.now()
        end = datetime.now()
        insert_last_item(DataItem.STOCK_LIST, start, end, 0)
    except Exception as e:
        logger.warn(f'fetch_stock_list() fail - {e}')
    logger.info('fetch_stock_list() end.')

def fetch_stock_history(**kwargs) -> None:
    logger.info('fetch_stock_history() start.')
    try:
        item = select_last_item(DataItem.STOCK_DAILY_HISTORY)
        start = datetime.now()
        end = datetime.now()

        if_exists='append'

        if item:
            start = utils.string2Datetime2(item['end']) + timedelta(days=1)
        else:
            start = HISTORY_START

        # print(f'start = {start}, end = {end}')
        if start < end:
            stock.fetch_history(start=utils.date2String2(start), end=utils.date2String2(end), period='daily', adjust='qfq', if_exists=if_exists)
            insert_last_item(DataItem.STOCK_DAILY_HISTORY, start, end, 0)
    except Exception as e:
        logger.warn(f'fetch_stock_history() fail - {e}')        
    logger.info('fetch_stock_history() end.')

def fetch_stock_margin(**kwargs):
    logger.info('fetch_stock_margin() start.')
    try:
        item = select_last_item(DataItem.STOCK_DAILY_MARGIN)
        start = datetime.now()
        end = datetime.now()

        if_exists='append'

        if item:
            start = utils.string2Datetime2(item['end']) + timedelta(days=1)
        else:
            start = HISTORY_START

        if start < end:
            stock.fetch_margin(start=utils.date2String2(start), end=utils.date2String2(end), if_exists=if_exists)
            insert_last_item(DataItem.STOCK_DAILY_MARGIN, start, end, 0)
    except Exception as e:
        logger.warn(f'fetch_stock_margin() fail - {e}')        
    logger.info('fetch_stock_margin() end.')

"""
incoude:
    stock history
    stock hsgt
    stock margin
"""
# def updateDailyStockData():
#     try:
#         stock.fetch_history(symbol=options['codes'], start=options['start'], end=options['end'], period='daily', adjust='qfq', if_exists=options['if_exits'])

#         stock.fetch_hsgt(symbol=options['codes'], start=options['start'], end=options['end'], if_exists='replace') # options['if_exits'])

#         stock.fetch_margin(symbol=options['codes'], start=options['start'], end=options['end'], if_exists=options['if_exits'])
#     except Exception as e:
#         logger.warn(f'updateDailyStockData() fail - {e}')