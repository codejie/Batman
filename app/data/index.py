"""
指数数据相关函数计划
"""

import pandas
from pandas import DataFrame

from app import logger, AppException
from app.dbengine import engine
from app.data.local_db import TableName

"""
查询A股指数列表
"""
def get_a_index(symbol: str = None) -> DataFrame:
    try:
        return pandas.read_sql_table(TableName.Index_A_List, engine)
    except Exception as e:
        raise AppException(e)
    
"""
查询指数历史数据
"""
def get_history(symbol: str, start_date: str, end_date: str, period: str = 'daily') -> DataFrame:
    try:
        table = TableName.make_index_history_name(symbol, period)
        sql = f'SELECT * FROM {table} WHERE "日期" >= "{start_date}" AND "日期" <= "{end_date}"'
        return pandas.read_sql_query(sql, engine)
    except Exception as e:
        raise AppException(e)    

# from pandas import DataFrame
# import akshare

# from .. import AppException
# from . import DataSource, DATA_SOURCE_REQUEST_TIMEOUT

# from .. import logger

# DATA_SOURCE = DataSource.AKSHARE

# def set_source(src: DataSource) -> None:
#     """
#     设置数据源
#     - ak: aksare
#     """
#     DATA_SOURCE = src

# def get_infos() -> DataFrame:
#     """
#     获取指数信息
#     """
#     try:
#         if DATA_SOURCE == DataSource.AKSHARE:
#             return akshare.index_stock_info()
#     except Exception as e:
#         logger.debug(e)
#         raise AppException(message='get_infos() fail.')
#     raise AppException(message=f'unknown data source - {DATA_SOURCE.name}')

# def get_history(symbol: str, start_date: str, end_date: str, period: str = 'daily') -> DataFrame:
#     """
#     获取单个指数历史数据
#     """
#     try:
#         if DATA_SOURCE == DataSource.AKSHARE:
#             return akshare.index_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date)
#     except Exception as e:
#         # logger.debug(e)
#         raise AppException(message='get_history() fail.')
#     raise AppException(message=f'unknown data source - {DATA_SOURCE.name}')
