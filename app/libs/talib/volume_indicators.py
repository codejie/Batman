"""
Volume Indicators
交易量指标
"""
import talib as ta
from pandas import Series

def OBV(value: Series, volume: Series) -> Series:
    """
    OBV - On Balance Volume
    real = OBV(close, volume)
    """
    return ta.OBV(value, volume)