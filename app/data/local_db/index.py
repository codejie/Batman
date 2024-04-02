"""
本地化指数数据函数集合
"""
from pandas import DataFrame
from app.dbengine import engine
from app import logger, AppException
from app.data.remote_api import index as remote
from app.data import index as local
from app.data.local_db import TableName
from app.routers import utils

"""
添加指数列表记录
"""
def append_a_index(**kwargs) -> None:
    try:
        logger.info('append_a_index() called.')
        df: DataFrame = DataFrame({
            'code': [kwargs['code']],
            'name': [kwargs['name']]
        })
        df.to_sql(TableName.Index_A_List, engine, if_exists='append', index=False)
        logger.info('append_a_index() end.')
    except Exception as e:
        raise AppException(e)

"""
获取本地所有指数的历史数据
"""
def fetch_history(**kwargs):
    try:
        logger.info('fetch_history() called.')
        symbol = kwargs['symbol']
        start_date = utils.dateConvert1(kwargs['start'])
        end_date = utils.dateConvert1(kwargs['end'])
        period = kwargs['period']
        if_exists = kwargs['if_exists']

        codes = local.get_a_index() if symbol is None else { 'code': [kwargs['code']], 'name': ['']}
        for code in codes['code']:
            table = TableName.make_index_history_name(code, period)
            df = remote.get_history(symbol=code, start_date=start_date, end_date=end_date, period=period)
            df.to_sql(table, engine, if_exists=if_exists, index=False)
        logger.info('fetch_history() end.')
    except Exception as e:
        raise AppException(e)