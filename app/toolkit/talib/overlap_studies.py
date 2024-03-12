"""
Overlap Studies 
重叠研究/指标
"""

import talib as ta
from pandas import DataFrame, Series
from ... import AppException

MATypes = ['SMA','EMA','WMA','DEMA','TEMA','TRIMA','KAMA','MAMA','T3']

"""
MA 移动平均线
"""
def MA(value: Series, period: int = 30, ma_type: str = 'SMA') -> Series:
    """
    MA - Moving average
    real = MA(close, timeperiod=30, matype=0)
    """
    try:
        return Series(name=f'{value.name}_{period}', data=ta.MA(value, period, MATypes.index(ma_type)))
    except Exception as e:
        raise AppException(-1, repr(e))


def MA_turbo(df: DataFrame, columns: list[str] | None = None, periods: list[int] = [5], types: list[str] = ['SMA']) -> DataFrame:
    """
    MA - Moving average
    real = MA(close, timeperiod=30, matype=0)
    types: 'SMA','EMA','WMA','DEMA','TEMA','TRIMA','KAMA','MAMA','T3'
    """
    try:
        ret = DataFrame()
        for type in types:
            if columns == None:
                for col in df.columns.values:
                    for period in periods:
                        i = MATypes.index(type)
                        ret[f'{col}_{type}{period}'] = ta.MA(df[col], period, i)
            else:
                for col in columns:
                    for period in periods:
                        i = MATypes.index(type)
                        ret[f'{col}_{type}{period}'] = ta.MA(df[col], period, i)
        return ret
    except Exception as e:
        raise AppException(-1, repr(e))
    
"""
Bollinger Band
布林带
"""
def BBANDS(value: Series, period: int = 5, nbdevup: int = 2, nbdevdn: int = 2, ma_type: str = 'SMA') -> DataFrame:
    """
    BBANDS - Bollinger Bands
    upperband, middleband, lowerband = BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    """
    try:
        ret = DataFrame()
        ret[f'{value.name}_upper'], ret[f'{value.value}_middle'], ret[f'{value.value}_lower'] = ta.BBANDS(value, period, nbdevup, nbdevdn, MATypes.index(ma_type))
        return ret
    except Exception as e:
        raise AppException(-1, repr(e))    

def BBANDS_turbo(df: DataFrame, columns: list[str] | None = None, period: int = 5, nbdevup: int = 2, nbdevdn: int = 2, types: list[str] = ['SMA']) -> DataFrame:
    """
    BBANDS - Bollinger Bands
    upperband, middleband, lowerband = BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    """
    # logger.debug(columns)
    # logger.debug(f'{period}-{nbdevup}-{nbdevdn}')
    # logger.debug(types)
    try:
        ret = DataFrame()
        for type in types:
            for col in (df.columns.values if columns == None else columns):
                ret[f'{col}_upper'], ret[f'{col}_middle'], ret[f'{col}_lower'] = ta.BBANDS(df[col], period, nbdevup, nbdevdn, MATypes.index(type))
        return ret
    except Exception as e:
        raise AppException(-1, repr(e)) 