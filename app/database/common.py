"""
数据库访问通用函数封装
"""
import pandas
from pandas import DataFrame

from app.database import dbEngine
from app.database.tables import TableName
from app.exception import AppDataException

def make_sql_select(table: str, columns: list[str] = None, where: str = None) -> str:
    sql = 'SELECT '
    if columns and len(columns) > 0:
        for i in range(len(columns)):
            sql += f'{columns[i]}{', ' if i < len(columns) - 1 else ''}'
    else:
        sql += '*'
    sql += f' FROM {table}'
    if where:
        sql += f' WHERE {where}'
    
    # print(f'sql={sql}')
    return sql

def select(table: str, columns: list[str] = None, where: str = None, column_trans: list[str] = None) -> DataFrame:
    try:
        sql = make_sql_select(table, columns, where)
        df = pandas.read_sql_query(sql, dbEngine.get_engine())
        if column_trans and columns:
            col_map = {}
            for i in range(len(columns)):
                if i < len(column_trans):
                    col_map[columns[i]] = column_trans[i]
            if len(col_map) > 0:
                df = df.rename(columns=col_map, copy=False)
        return df
    except Exception as e:
        raise AppDataException(e)