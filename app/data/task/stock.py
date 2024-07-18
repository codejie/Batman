"""
Stock data init
"""
from datetime import datetime
from pandas import DataFrame

from app.exception import AppException
from app.database import dbEngine, sql_select, func
from app.database.tables import StockAListTable
from app.data.local_db import stock as local
from app.data.task import records
from app.logger import logger

"""
init check
"""
def init_check() -> None:
    try:
        if not exist_list_table():
            start = records.HISTORY_START
            end = datetime.now()
            init_list(start=start, end=end)

            symbols = get_list()
            # symbols = symbols.iloc[2:6]
            # print(f'=====\n{symbols}')

            init_daily_history(symbols=symbols, start=start, end=end)
            init_hsgt(symbols=symbols, start=start, end=end)
            init_margin(symbols=symbols, start=start, end=end)      
        
    except Exception as e:
        raise AppException(e)

def exist_list_table() -> bool:
    stmt = sql_select(func.count()).select_from(StockAListTable)
    result = dbEngine.select_one(stmt)
    return result > 0

def init_list(start: datetime, end: datetime) -> None:
    local.fetch_a_list(if_exists='replace')
    records.insert(records.Item.STOCK_LIST, end)

def get_list() -> DataFrame:    
    return local.get_a_list()

def init_daily_history(symbols: DataFrame, start: datetime, end: datetime) -> None:
     for i, r in symbols.iterrows():
        code = r['code']
        local.fetch_history(code, start, end, if_exists='replace')
        records.insert(records.Item.STOCK_DAILY_HISTORY, end, code)

def init_hsgt(symbols: DataFrame, start: datetime, end: datetime) -> None:
    for i, r in symbols.iterrows():
        try:
            code = r['code']
            local.fetch_hsgt(code, 'replace')
            records.insert(records.Item.STOCK_DAILY_HSGT, end, code)
        except Exception as e:
            logger.warn(f'stock {code} fetch_hsgt() fail - {e}')

def init_margin(symbols: DataFrame, start: datetime, end: datetime) -> None:
    codes = symbols['code'].to_list()
    local.fetch_margin(codes, start, end, 'append')
    records.insert(records.Item.STOCK_DAILY_MARGIN, end)

"""
daily update
"""
def update_daily() -> None:
    try:
        symbols = get_list()
        update_daily_history(symbols=symbols)
        update_hsgt(symbols=symbols)
        update_margin(symbols=symbols)
    except Exception as e:
        raise AppException(e)
    
def update_daily_history(symbols: DataFrame) -> None:
     for i, r in symbols.iterrows():
        code = r['code']
        start, end, is_update = records.get_start_end(records.Item.STOCK_DAILY_HISTORY, code)
        # print(f'{code} - {start} - {end} - {is_update} ------ update daily_history')        
        if start < end:
            local.fetch_history(code, start, end, if_exists='append')
            records.set_latest(records.Item.STOCK_DAILY_HISTORY, end, code, is_update)

def update_hsgt(symbols: DataFrame) -> None:
    for i, r in symbols.iterrows():
        try:
            code = r['code']
            start, end, is_update = records.get_start_end(records.Item.STOCK_DAILY_HSGT, code)
            if start < end:
                local.fetch_hsgt(code, 'append')
                records.set_latest(records.Item.STOCK_DAILY_HSGT, end, code, is_update)
        except Exception as e:
            logger.warn(f'stock {code} fetch_hsgt() fail - {e}')

def update_margin(symbols: DataFrame) -> None:
    start, end, is_update = records.get_start_end(records.Item.STOCK_DAILY_MARGIN)
    if start < end:
        codes = symbols['code'].to_list()
        local.fetch_margin(codes, start, end, 'append')
        records.set_latest(records.Item.STOCK_DAILY_MARGIN, end, is_update=is_update)    

