"""
数据任务
"""
from enum import Enum
from datetime import datetime, timedelta

from app import logger
from app.dbengine import engine, text
from app.data.local_db import stock

TABLE_SYSTEM_DATA_UPDATED_RECORD = 'sys_data_updated_record'

class DataItem(Enum):
    STOCK_LIST = 1
    STOCK_DAILY_HISTORY = 2
    STOCK_DAILY_HSGT = 3
    STOCK_DAILY_MARGIN = 4


    INDEX_LIST = 1000

def select_last_item(item: DataItem) -> dict:
    data = {
        'item': item.value
    }
    stmt = text(f'SELECT start, end, result, arg1, arg2 FROM {TABLE_SYSTEM_DATA_UPDATED_RECORD} WHERE item==:item ORDER BY ID DESC LIMIT 1')
    with engine.connect() as conn:
        results = conn.execute(stmt, data)
        if results is not None:
        else:




"""
System Data Check
"""
async def system_data_updated_check():
    logger.info('system_data_updated_check() start.')


    # STOCK_LIST
    await check_stock_list()


    logger.info('system_data_updated_check() end.')


"""
Stock List check
"""
async def check_stock_list():



"""
incoude:
    stock history
    stock hsgt
    stock margin
"""
def updateDailyStockData():
    try:
        stock.fetch_history(symbol=options['codes'], start=options['start'], end=options['end'], period='daily', adjust='qfq', if_exists=options['if_exits'])

        stock.fetch_hsgt(symbol=options['codes'], start=options['start'], end=options['end'], if_exists='replace') # options['if_exits'])

        stock.fetch_margin(symbol=options['codes'], start=options['start'], end=options['end'], if_exists=options['if_exits'])
    except Exception as e:
        logger.warn(f'updateDailyStockData() fail - {e}')