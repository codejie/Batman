"""
通用股票数据函数集合
"""
import pandas
from pandas import DataFrame
from app.data.local_db import TableName
from app.dbengine import engine

def get_daily_history_quote(code: str, date: str, period: str='daily', adjust: str='qfq') -> DataFrame:
    table = TableName.make_stock_history_name(symbol=code, period=period, adjust=adjust)
    sql = None
    if date:
        sql = f'SELECT * FROM {table} WHERE 日期 == "{date}" LIMIT 1'
    else:
        sql = f'SELECT * FROM {table} ORDER BY 日期 DESC LIMIT 1'

    return pandas.read_sql_query(sql, engine)        
