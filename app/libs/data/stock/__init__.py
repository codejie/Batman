"""
## 股票相关的函数集合
- set_source
"""

from enum import Enum
from pandas import DataFrame
import akshare

from .... import AppException

from .... import logger

DATA_SOURCE_REQUEST_TIMEOUT = 60

class DataSource(Enum):
    """
    UNKNOWN = 'ukn'
    AKSHARE = 'akshare'
    """
    UNKNOWN = 'ukn'
    AKSHARE = 'akshare'

DATA_SOURCE_STOCK = DataSource.AKSHARE

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
        if DATA_SOURCE_STOCK == DataSource.AKSHARE:
            return akshare.stock_individual_info_em(symbol=symbol, timeout=DATA_SOURCE_REQUEST_TIMEOUT)
    except:
        raise AppException(message='get_individual_info() fail.')
    raise AppException(message=f'unknown data source - {DATA_SOURCE_STOCK.name}')
    
def get_history(symbol: str, start_date: str, end_date: str, period: str = 'daily', adjust: str = 'hfq'):
    """
    获取个股历史数据
    """
    try:
        if DATA_SOURCE_STOCK == DataSource.AKSHARE:
            logger.debug(f'{start_date} - {end_date} - {period} - {adjust} - {symbol}')
            return akshare.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust=adjust, timeout=DATA_SOURCE_REQUEST_TIMEOUT)
    except:
        raise AppException(message='get_history() fail.')
    raise AppException(message=f'unknown data source - {DATA_SOURCE_STOCK.name}')