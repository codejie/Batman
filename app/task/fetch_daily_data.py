"""
每日数据下载
"""
from app import logger
from app.dbengine import engine, text
from app.data import stock
from app.data.local_db import stock as local

from app.task.item_updated import DataItem, get_item_start_end, set_item_latest


def fetch_data(**kwargs):
    logger.info('fetch_daily_data check() start.')

    # kwargs['end'] = utils.date2String2(datetime.now()) 

    # STOCK_DIALIY_HISTORY
    fetch_stock_history(**kwargs)

    # STOCK_DAILY_HSGT
    fetch_stock_hsgt(**kwargs)

    logger.info('fetch_daily_data check() end.')

def fetch_stock_history(**kwargs):
    logger.info('-- fetch_stock_history() start.')

    symbols = stock.get_a_list()
    
    # check
    kwargs['period'] = 'daily'
    kwargs['adjust'] = 'qfq'
    kwargs['if_exists'] = 'append'

    for index, row in symbols.iterrows():
        kwargs['symbol'] = row['code']
        kwargs['start'], kwargs['end'], insert = get_item_start_end(DataItem.STOCK_DAILY_HISTORY, kwargs['symbol'])
        if kwargs['start'] and kwargs['end']:
            local.fetch_history(**kwargs)
            set_item_latest(DataItem.STOCK_DAILY_HISTORY, kwargs['end'], kwargs['symbol'], insert)

    logger.info('-- fetch_stock_history() end.')

def fetch_stock_hsgt(**kwargs):
    logger.info('-- fetch_stock_hsgt() start.')

    symbols = stock.get_a_list()
    
    # check
    kwargs['if_exists'] = 'append'

    for index, row in symbols.iterrows():
        kwargs['symbol'] = row['code']
        kwargs['start'], kwargs['end'], insert = get_item_start_end(DataItem.STOCK_DAILY_HSGT, kwargs['symbol'])
        if kwargs['start'] and kwargs['end']:
            local.fetch_hsgt(**kwargs)
            set_item_latest(DataItem.STOCK_DAILY_HSGT, kwargs['end'], kwargs['symbol'], insert)

    logger.info('-- fetch_stock_hsgt() end.')





