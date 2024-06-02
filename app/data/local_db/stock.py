"""
Stock本地化函数
"""
import pandas
from pandas import DataFrame
from datetime import datetime, timedelta

from app.utils import debug
from app.logger import logger
from app.exception import AppDataException
from app.data.remote_api import stock as remote
from app.database import dbEngine
from app.database.tables import TableName
from app.utils import utils

"""
获取A股列表
"""
def fetch_a_list(if_exists: str = 'replace') -> None:
    logger.debug(f'{debug.__function__()}() called')
    df = remote.get_a_code()
    if not df.empty:
        df.to_sql(TableName.Stock_A_List, dbEngine.get_engine(), if_exists=if_exists, index=False)
    logger.debug(f'{debug.__function__()}() called end')
"""
get A股列表
"""
def get_a_list() -> DataFrame:
    return pandas.read_sql_table(TableName.Stock_A_List, dbEngine.get_engine())

"""
获取股票历史数据
"""
def fetch_history(code: str, start: datetime, end: datetime, period: str = 'daily', adjust: str = 'qfq', if_exists='replace') -> None:
    logger.debug(f'{code} - {debug.__function__()}() called')
    start = utils.date2String1(start)
    end = utils.date2String1(end)
    df = remote.get_history(code, start, end, period, adjust)
    if not df.empty:
        table = TableName.make_stock_history_name(code, period, adjust)
        df.to_sql(name=table, con=dbEngine.get_engine(), if_exists=if_exists, index=False)
    logger.debug(f'{debug.__function__()}() called end')

"""
个股深沪港股通持股数据（北向资金）
""" 
def fetch_hsgt(code: str, if_exists: str = 'replace') -> None:
    logger.debug(f'{code} - {debug.__function__()}() called')
    df = remote.get_individual_hsgt(code)
    if not df.empty:
        table = TableName.make_stock_hsgt_name(code)
        df = df[::-1]
        df.to_sql(name=table, con=dbEngine.get_engine(), if_exists=if_exists, index=False)
    logger.debug(f'{debug.__function__()}() called end')

"""
个股融资融券数据
"""
def fetch_margin(codes: list, start: datetime, end: datetime, if_exists: str = 'append') -> None:
    logger.debug(f'{utils.date2String2(start)} - {debug.__function__()}() called')
    delta = timedelta(days=1)
    while start <= end:
        try:
            df = remote.get_margin(utils.date2String1(start))
            if not df.empty: 
                df.insert(2, '日期', utils.date2String2(start))
                for i in range(len(df)):
                    sdf = df.iloc[i:i+1]
                    code = sdf.iloc[0]['证券代码']
                    if code in codes:
                        table = TableName.make_stock_margin_name(code)
                        sdf = sdf.iloc[:,2:]
                        sdf.to_sql(name=table, con=dbEngine.get_engine(), if_exists=if_exists, index=False)
        except Exception as e:
            logger.warn(f'{utils.date2String2(start)} fetch_margin() fail - {e}')
        start += delta
    logger.debug(f'{debug.__function__()}() called end')
