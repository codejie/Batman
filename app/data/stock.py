"""
Local股票数据相关的函数集合
(should not use those functions directly)
"""
import pandas
from pandas import DataFrame

from app import logger, AppException
from app.dbengine import engine
from app.data.local_db import TableName
from app.data.remote_api import stock as remote

"""
获取A股股票列表
"""
def get_a_list(symbol: str = None) -> DataFrame:
    try:
        return pandas.read_sql_table(TableName.Stock_A_List, engine)
    except Exception as e:
        raise AppException(e)

"""
获取个股历史数据
"""
def get_history(symbol: str, start_date: str, end_date: str, period: str = 'daily', adjust: str = 'qfq') -> DataFrame:
    try:
        table = TableName.make_stock_history_name(symbol, period, adjust)
        sql = f'SELECT * FROM {table} WHERE "日期" >= "{start_date}" AND "日期" <= "{end_date}"'
        # print(sql)
        return pandas.read_sql_query(sql, engine)
    except Exception as e:
        raise AppException(e)
    
"""
获取股票个股信息
"""    
def get_individual_info(symbol: str) -> DataFrame:
    return remote.get_individual_info(symbol)

"""
查询个股持股数据
"""
def get_hsgt(symbol: str, start_date: str, end_date: str) -> DataFrame:
    try:
        table = TableName.make_stock_hsgt_name(symbol)
        sql = f'SELECT * FROM {table} WHERE "持股日期" >= "{start_date}" AND "持股日期" <= "{end_date}" ORDER BY "持股日期"'
        # print(sql)
        return pandas.read_sql_query(sql, engine)
    except Exception as e:
        raise AppException(e)    

"""
查询个股融资融券数据
"""
def get_margin(symbol: str, start_date: str, end_date: str) -> DataFrame:
    try:
        table = TableName.make_stock_margin_name(symbol)
        sql = f'SELECT * FROM {table} WHERE "日期" >= "{start_date}" AND "日期" <= "{end_date}"'
        return pandas.read_sql_query(sql, engine)
    except Exception as e:
        raise AppException(e)        