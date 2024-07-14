"""
股票类常用函数封装
"""
from pandas import DataFrame
from app.database import common, tables

def get_a_list() -> DataFrame:
    return common.select(tables.TableName.Stock_A_List)

def get_history(code: str, start: str, end: str, columns: list[str] = None, peroid: str = 'daily', adjust: str = 'qfq') -> DataFrame:
    table = tables.TableName.make_stock_history_name(code, peroid, adjust)
    where = f'日期 >="{start}" AND 日期 <= "{end}" order by 日期'
    return common.select(table, columns, where)
