"""
本地化股票数据函数集合
"""
from app.dbengine import engine
from app import logger, AppException
from app.data.remote_api import stock as remote
from app.data import stock as local
from app.data.local_db import TableName
from app.routers import utils

"""
获取A股所有股票代码
"""
def fetch_a_stock(**kwargs) -> None:
    try:
        logger.info('fetch_a_stock called.')
        df = remote.get_a_code()
        df.to_sql(TableName.Stock_A_List, engine, if_exists=kwargs['if_exists'], index=False)    
        logger.info('fetch_a_stock() end.')
    except Exception as e:
        logger.error(f'fetch_stock() fail - {e.message}')

"""
获取A股所有股票历史数据
"""
def fetch_all_history(**kwargs) -> None:
    try:
        symbol = kwargs['symbol']
        start_date = utils.dateConvert1(kwargs['start']),
        end_date = utils.dateConvert1(kwargs['end']),
        period = kwargs['period']
        adjust = kwargs['adjust']
        if_exists = kwargs['if_exists']

        logger.info('fetch_all_stock_history() called.')
        codes = local.get_a_code() if symbol is None else { 'code': [symbol], 'name': ['']}
        for code in codes['code']:
            table = TableName.make_stock_history_name(code, period, adjust)
            df = remote.get_history(code, start_date, end_date, period, adjust)
            df.to_sql(table, engine, if_exists=if_exists, index=False)
        logger.info('fetch_all_stock_history() end.')
    except Exception as e:
        logger.error(f'fetch_all_stock_history() fail - {e}')

def fetch_test(**kwargs):
    logger.error('err')
