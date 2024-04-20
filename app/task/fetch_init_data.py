"""
系统数据初始
"""
from datetime import datetime, timedelta

from app import logger, utils
from app.dbengine import engine, text

from app.data.local_db import TableName, stock as local
from app.data import stock
from app.task.item_updated import DataItem, select_item_latest, insert_item_latest

HISTORY_START =  datetime(year=2022, month=1, day=1)

def init_check(**kwargs) -> bool:
    if not check(**kwargs):
        init_daily_data(**kwargs)
        return True
    else:
        return False

def check(**kwargs) -> bool:
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
    # STOCK LIST
    local.fetch_a_stock(if_exists='replace')
    insert_item_latest(DataItem.STOCK_LIST, latest)

    kwargs['start'] = utils.date2String2(HISTORY_START)
    kwargs['end'] = latest
    kwargs['period'] = 'daily'
    kwargs['adjust'] = 'qfq'
    kwargs['if_exists'] = 'replace'

    # STOCK DAILY
    init_daily_stock(**kwargs)


def init_daily_stock(**kwargs):
    symbols = stock.get_a_list()

    # history
    for index, row in symbols.iterrows():
        # print(f'symbol = {row}')
        kwargs['symbol'] = row['code']
        logger.debug(f'init stock - {kwargs}')
        local.fetch_history(**kwargs)
        insert_item_latest(DataItem.STOCK_DAILY_HISTORY, kwargs['end'], row['code'])

    # margin
    kwargs['symbol'] = symbols['code'].to_list()
    kwargs['if_exists'] = 'append'
    local.fetch_margin(**kwargs)
    insert_item_latest(DataItem.STOCK_DAILY_MARGIN, kwargs['end'])













