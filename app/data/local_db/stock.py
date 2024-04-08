"""
本地化股票数据函数集合
"""
from datetime import timedelta
from pandas import DataFrame
from app.dbengine import engine
from app import logger, AppException
from app.data.remote_api import stock as remote
from app.data import stock as local
from app.data.local_db import TableName
from app.routers import utils

"""
获取A股所有股票代码
"""
def fetch_a_stock(**kwargs) -> None:
    try:
        logger.info('fetch_a_stock called.')
        df = remote.get_a_code()
        df.to_sql(TableName.Stock_A_List, engine, if_exists=kwargs['if_exists'], index=False)    
        logger.info('fetch_a_stock() end.')
    except Exception as e:
        logger.error(f'fetch_stock() fail - {e.message}')

"""
获取A股所有股票历史数据
"""
def fetch_history(**kwargs) -> None:
    try:
        symbol = kwargs['symbol'] if 'symbol' in kwargs else None
        start_date = utils.dateConvert1(kwargs['start'])
        end_date = utils.dateConvert1(kwargs['end'])
        period = kwargs['period']
        adjust = kwargs['adjust']
        if_exists = kwargs['if_exists']

        logger.info('fetch_all_stock_history() called.')

        codes = local.get_a_list() if symbol is None else DataFrame().from_dict(symbol)        
        for code in codes['code']:
            table = TableName.make_stock_history_name(code, period, adjust)
            df = remote.get_history(code, start_date, end_date, period, adjust)
            df.to_sql(table, engine, if_exists=if_exists, index=False)

        logger.info('fetch_all_stock_history() end.')
    except Exception as e:
        logger.error(f'fetch_all_stock_history() fail - {e}')

"""
个股持股数据
"""
def fetch_hsgt(**kwargs) -> None:
    # try:
    symbol = kwargs['symbol'] if 'symbol' in kwargs else None
    if_exists = kwargs['if_exists']
    logger.info('fetch_hsgt() called.')
    codes = local.get_a_list() if symbol is None else DataFrame().from_dict(symbol)
    for code in codes['code']:
        try:
            df = remote.get_individual_hsgt(code)
            table = TableName.make_stock_hsgt_name(code)
            if df is not None:
                df.to_sql(table, engine, if_exists=if_exists, index=False)
            else:
                logger.warn(f'fetch_hsgt() {code} data is None.')
        except Exception as e:
            logger.warn(f'fetch_hsgt() fetch {code} data fail - {e}')
    logger.info('fetch_hsgt() end.')
    # except Exception as e:
    #     logger.error(f'fetch_hsgt() fail - {e}')

"""
个股融资融券数据
"""
def fetch_margin(**kwargs) -> None:
    try:
        symbol = kwargs['symbol'] if 'symbol' in kwargs else None
        start_date = utils.string2Date2(kwargs['start'])
        end_date = utils.string2Date2(kwargs['end'])      
        if_exists = kwargs['if_exists']
        logger.info('fetch_margin() called.')

        delta = timedelta(days=1)
        while start_date <= end_date:
            code = None
            try:
                df = remote.get_margin(utils.date2String1(date=start_date))
                if df is not None:
                    df.insert(2, '日期', utils.date2String2(date=start_date))
                    for i in range(len(df)):
                        sdf = df.iloc[i:i+1]
                        code = sdf.iloc[0]['证券代码']
                        table = TableName.make_stock_margin_name(symbol=code)
                        sdf = sdf.iloc[:,2:]
                        sdf.to_sql(table, engine, if_exists=if_exists, index=False)
                else:
                    logger.warn(f'fetch_margin() fetch {code} data None.')
            except Exception as e:
                logger.warn(f'fetch_margin() fetch {code} data fail - {e}')
            start_date += delta            
        logger.info('fetch_margin() end.')
    except Exception as e:
        logger.error(f'fetch_margin() fail - {e}')