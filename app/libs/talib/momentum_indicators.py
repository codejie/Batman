"""
Momentum Indicator
动量指标类
"""
import talib as ta
from pandas import Series, DataFrame

from app.exception import AppException

def MACD(value: Series, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> DataFrame:
    """
    MACD - Moving Average Convergence/Divergence
    macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    """
    try:
        ret = DataFrame()
        ret['dif'], ret['dea'], ret['macd'] = ta.MACD(value, fast_period, slow_period, signal_period)
        return ret
    except Exception as e:
        raise AppException(-1, repr(e))    

def MACD_turbo(df: DataFrame, columns: list[str] | None = None, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> DataFrame:
    """
    MACD - Moving Average Convergence/Divergence
    macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    """
    try:
        ret = DataFrame()
        for col in df.columns.values:
            ret[f'{col}_dif'], ret[f'{col}_dea'], ret[f'{col}_macd'] = ta.MACD(df[col], fast_period, slow_period, signal_period)
        return ret
    except Exception as e:
        raise AppException(-1, repr(e))

def RSI(value: Series, period: int = 14) -> Series:
    """
    RSI - Relative Strength Index
    real = RSI(close, timeperiod=14)

    NOTE: The RSI function has an unstable period.
    """
    try:
        return Series(name=f'{value.name}_rsi', data=ta.RSI(value, period))
    except Exception as e:
        raise AppException(-1, repr(e))