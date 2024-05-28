"""
数据配置定义
"""

from enum import Enum

DATA_SOURCE_REQUEST_TIMEOUT = 60

class DataSource(Enum):
    """
    UNKNOWN = 'ukn'
    AKSHARE = 'akshare'
    """
    UNKNOWN = 'ukn'
    AKSHARE = 'akshare'