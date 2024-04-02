"""
股票数据相关的函数集合
- set_source
"""

from pandas import DataFrame
from typing import List
import akshare

from app import logger, AppException
from app.data.remote_api import DataSource, DATA_SOURCE_REQUEST_TIMEOUT
from app.toolkit import adapter

DATA_SOURCE = DataSource.AKSHARE

def set_source(src: DataSource) -> None:
    """
    设置数据源
    - ak: aksare
    """
    DATA_SOURCE = src

def get_a_code(market: str | None = None) -> DataFrame:
    """
    获取A股股票列表
    market:
        None: all
        sh: 上交所
        sz: 深交所
        bj: 北交所
    """
    try:
        if DATA_SOURCE == DataSource.AKSHARE:
            if market == 'sh':
                return akshare.stock_info_sh_name_code(symbol='主板A股')
            elif market == 'sz':
                return akshare.stock_info_sz_name_code(symbol='A股列表')
            elif market == 'bj':
                return akshare.stock_info_bj_name_code()
            else:
                return akshare.stock_info_a_code_name()
        else:
            raise AppException(message=f'unknown data source - {DATA_SOURCE.name}')
    except Exception as e:
        raise AppException(e)

def get_individual_info(symbol: str) -> DataFrame:
    """
    获取股票个股信息
    """
    # logger.debug(symbol)
    try:
        if DATA_SOURCE == DataSource.AKSHARE:
            return akshare.stock_individual_info_em(symbol=symbol, timeout=DATA_SOURCE_REQUEST_TIMEOUT)
        else:
            raise AppException(message=f'unknown data source - {DATA_SOURCE.name}')
    except Exception as e:
        raise AppException(e)
    
def get_history(symbol: str, start_date: str, end_date: str, period: str = 'daily', adjust: str = 'qfq') -> DataFrame:
    """
    获取个股历史数据
    """
    try:
        if DATA_SOURCE == DataSource.AKSHARE:
            # logger.debug(f'{start_date} - {end_date} - {period} - {adjust} - {symbol}')
            df = akshare.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust, timeout=DATA_SOURCE_REQUEST_TIMEOUT)
            cols = adapter.columns_akshare2standard(df.columns)
            return df.rename(columns=cols)
        else:
            raise AppException(message=f'unknown data source - {DATA_SOURCE.name}')
    except Exception as e:
        raise AppException(e)


def get_spot(symbols: List[str] | None = None) -> DataFrame:
    """
    获取A股实时行情数据
    """
    try:
        if DATA_SOURCE == DataSource.AKSHARE:
            df = akshare.stock_zh_a_spot_em()
            if symbols != None and len(symbols) > 0:
                # logger.debug(symbols)
                df = df[df['代码'].isin(symbols)]
            return df.head()
        else:
            raise AppException(message=f'unknown data source - {DATA_SOURCE.name}')
    except Exception as e:
        raise AppException(e)