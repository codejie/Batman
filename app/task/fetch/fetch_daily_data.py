"""
每日数据下载
"""
from datetime import datetime

from app import logger
from app.dbengine import engine, text
from app.data import stock
from app.data.local_db import stock as local

from app.task.fetch.item_updated import DataItem, get_item_start_end, set_item_latest


def fetch_data(**kwargs):
    now = datetime.now()
    if (now.hour > 9 and now.hour < 16) or now.weekday() > 4:
        logger.debug('exchange time, fetch data skip..')
        return

    logger.info('fetch_daily_data check() start.')

    # kwargs['end'] = utils.date2String2(datetime.now()) 
    fetch_stock_data(**kwargs)

    logger.info('fetch_daily_data check() end.')

def fetch_stock_data(**kwargs):

    kwargs['symbols'] = stock.get_a_list()

    # STOCK_DIALIY_HISTORY
    fetch_stock_history(**kwargs)

    # STOCK_DAILY_HSGT
    fetch_stock_hsgt(**kwargs)

    # STOCK_DAILY_MARGIN
    fetch_stock_margin(**kwargs)

def fetch_stock_history(**kwargs):
    logger.info('-- fetch_stock_history() start.')

    symbols = kwargs['symbols'] # stock.get_a_list()

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

    symbols = kwargs['symbols']

    kwargs['if_exists'] = 'append'

    for index, row in symbols.iterrows():
        kwargs['symbol'] = row['code']
        kwargs['start'], kwargs['end'], insert = get_item_start_end(DataItem.STOCK_DAILY_HSGT, kwargs['symbol'])
        if kwargs['start'] and kwargs['end']:
            try:
                local.fetch_hsgt(**kwargs)
                set_item_latest(DataItem.STOCK_DAILY_HSGT, kwargs['end'], kwargs['symbol'], insert)
            except Exception as e:
                logger.warn(f'-- fetch_stock_hsgt() {kwargs['symbol']} data fail - {e}')

    logger.info('-- fetch_stock_hsgt() end.')

def fetch_stock_margin(**kwargs):
    logger.info('-- fetch_stock_margin() start.')

    kwargs['symbol'] = kwargs['symbols']['code'].to_list()
    kwargs['if_exists'] = 'append'

    kwargs['start'], kwargs['end'], insert = get_item_start_end(DataItem.STOCK_DAILY_MARGIN)
    if kwargs['start'] and kwargs['end']:
        try:
            local.fetch_margin(**kwargs)
            set_item_latest(DataItem.STOCK_DAILY_MARGIN, kwargs['end'], None, insert)
        except Exception as e:
            logger.warn(f'-- fetch_stock_margin() fail - {e}')
    logger.info('-- fetch_stock_margin() end.')    





