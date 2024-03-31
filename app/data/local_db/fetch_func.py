"""
获取数据函数集合
"""
from app.dbengine import engine
from app import logger, AppException
from app.data.remote_api import stock as remote_stock
from app.data import stock as local_stock
from app.data.local_db.define import TableName

"""
获取A股所有股票代码
"""
def fetch_a_stock(action: str = 'replace') -> None:
    try:
        logger.info('fetch_a_stock called.')
        df = remote_stock.get_a_code()
        df.to_sql(TableName.A_Stock, engine, if_exists='replace', )    
        logger.info('fetch_a_stock() end.')
    except Exception as e:
        logger.error(f'fetch_stock() fail - {e.message}')

"""
获取A股所有股票历史数据
"""
def fetch_all_stock_history( start_date: str, end_date: str, period: str = 'daily', adjust: str = 'qfq', action: str = 'append') -> None:
    try:
        logger.info('fetch_all_stock_history() called.')
        codes = local_stock.get_a_code()
        for code in codes['code']:
            table = TableName.make_stock_history_name(code, period, adjust)
            df = remote_stock.get_history(code, start_date, end_date, period, adjust)
            df.to_sql(table, engine, if_exists=action)
        logger.info('fetch_all_stock_history() end.')
    except Exception as e:
        logger.error(f'fetch_all_stock_history() fail - {e.message}')