"""
指数数据相关函数计划
"""
from pandas import DataFrame
import akshare

from .. import AppException
from . import DataSource, DATA_SOURCE_REQUEST_TIMEOUT

from .. import logger

DATA_SOURCE = DataSource.AKSHARE

def set_source(src: DataSource) -> None:
    """
    设置数据源
    - ak: aksare
    """
    DATA_SOURCE_STOCK = src

def get_infos() -> DataFrame:
    """
    获取指数信息
    """
    try:
        if DATA_SOURCE == DataSource.AKSHARE:
            return akshare.index_stock_info()
    except Exception as e:
        logger.debug(e)
        raise AppException(message='get_infos() fail.')
    raise AppException(message=f'unknown data source - {DATA_SOURCE.name}')

def get_history(symbol: str, start_date: str, end_date: str, period: str = 'daily') -> DataFrame:
    """
    获取单个指数历史数据
    """
    try:
        if DATA_SOURCE == DataSource.AKSHARE:
            return akshare.index_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date)
    except Exception as e:
        # logger.debug(e)
        raise AppException(message='get_history() fail.')
    raise AppException(message=f'unknown data source - {DATA_SOURCE.name}')
