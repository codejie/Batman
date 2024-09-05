"""
指数类常用函数封装
"""
from pandas import DataFrame
from app.database import common, tables

def get_a_list() -> DataFrame:
  return common.select(tables.TableName.Index_A_List)

def get_info(code: str) -> DataFrame:
  return common.select(table=tables.TableName.Index_A_List, columns=['index_code', 'display_name'], column_trans=['code', 'name'])
