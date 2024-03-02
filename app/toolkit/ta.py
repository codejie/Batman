"""
TA-Lib技术分析函数集合
"""

import talib as ta
from pandas import DataFrame, Series


def MA(type: str, ds: Series, period: int) -> Series:
    ret = Series(type)
    ret = ta.MA(ds, period, type)
    return ret