"""
## 股票数据相关的函数集合
- set_source
"""

from pandas import DataFrame
from typing import List
import akshare

from .. import AppException
from .. import logger
from . import DataSource, DATA_SOURCE_REQUEST_TIMEOUT


DATA_SOURCE = DataSource.AKSHARE

def set_source(src: DataSource) -> None:
    """
    设置数据源
    - ak: aksare
    """
    DATA_SOURCE_STOCK = src

def get_individual_info(symbol: str) -> DataFrame:
    """
    获取股票个股信息
    """
    logger.debug(symbol)
    try:
        if DATA_SOURCE == DataSource.AKSHARE:
            return akshare.stock_individual_info_em(symbol=symbol, timeout=DATA_SOURCE_REQUEST_TIMEOUT)
    except:
        raise AppException(message='get_individual_info() fail.')
    raise AppException(message=f'unknown data source - {DATA_SOURCE.name}')
    
def get_history(symbol: str, start_date: str, end_date: str, period: str = 'daily', adjust: str = 'hfq') -> DataFrame:
    """
    获取个股历史数据
    """
    try:
        if DATA_SOURCE == DataSource.AKSHARE:
            # logger.debug(f'{start_date} - {end_date} - {period} - {adjust} - {symbol}')
            return akshare.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust, timeout=DATA_SOURCE_REQUEST_TIMEOUT)
    except:
        raise AppException(message='get_history() fail.')
    raise AppException(message=f'unknown data source - {DATA_SOURCE.name}')

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
    except Exception as e:
        raise AppException(e)
    raise AppException(message=f'unknown data source - {DATA_SOURCE.name}')