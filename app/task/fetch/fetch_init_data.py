"""
系统数据初始
"""
from datetime import datetime, timedelta

from app import logger, utils
from app.dbengine import engine, text

from app.data.local_db import TableName, stock as local
from app.data import stock
from app.task.fetch.item_updated import DataItem, HISTORY_START, insert_item_latest

def init_check(**kwargs) -> bool:
    if not check(**kwargs):
        init_daily_data(**kwargs)
        return True
    else:
        return False

def check(**kwargs) -> bool:
    # return False
    # check stock list table
    try:
        stmt = text(f'SELECT count(*) FROM sqlite_master WHERE name="{TableName.Stock_A_List}"')
        with engine.connect() as conn:
            results = conn.execute(stmt)
            if results:
                result = results.first()
                if result and result[0] == 1:
                    return True
        return False
    except Exception as e:
        logger.info(f'init check() exception - {e}')
        return False

def init_daily_data(**kwargs):
    latest = utils.date2String2(datetime.now())
    # latest = '2024-01-01'
    # STOCK LIST
    local.fetch_a_stock(if_exists='replace')
    insert_item_latest(DataItem.STOCK_LIST, latest)

    kwargs['start'] = utils.date2String2(HISTORY_START)
    kwargs['end'] = latest

    # STOCK DAILY
    init_daily_stock(**kwargs)


def init_daily_stock(**kwargs):
    symbols = stock.get_a_list()
    kwargs['period'] = 'daily'
    kwargs['adjust'] = 'qfq'
    kwargs['if_exists'] = 'replace'    

    # history
    for index, row in symbols.iterrows():
        # print(f'symbol = {row}')
        kwargs['symbol'] = row['code']
        local.fetch_history(**kwargs)
        insert_item_latest(DataItem.STOCK_DAILY_HISTORY, kwargs['end'], kwargs['symbol'])

    # hsgt
    for index, row in symbols.iterrows():
        kwargs['symbol'] = row['code']
        try:
            local.fetch_hsgt(**kwargs)
            insert_item_latest(DataItem.STOCK_DAILY_HSGT, kwargs['end'], kwargs['symbol'])
        except Exception as e:
            logger.info(f'{kwargs['symbol']} hsgt data init failed - {e}')

    # margin
    kwargs['symbol'] = symbols['code'].to_list()
    kwargs['if_exists'] = 'append'
    local.fetch_margin(**kwargs)
    insert_item_latest(DataItem.STOCK_DAILY_MARGIN, kwargs['end'])














