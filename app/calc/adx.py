import pandas as pd
import talib

"""
### Result: DataFrame
- ADX: 0 - 100
- +DI
- -DI
- Signal: -1: downtrend, 0: neutral, 1: uptrend
"""

def calc(data: pd.DataFrame, period: int = 14, signal: bool = False, columns: list[str] = ['最高', '最低', '收盘']) -> pd.DataFrame:
    """
    计算ADX指标。

    Args:
        data (pd.DataFrame): 包含 'high', 'low', 'close' 列的历史数据。
        period (int): ADX计算周期，默认为14。

    Returns:
        pd.DataFrame: 包含ADX, +DI, -DI列的DataFrame。
    """
    adx = talib.ADX(data[columns[0]], data[columns[1]], data[columns[2]], timeperiod=period)
    plus_di = talib.PLUS_DI(data[columns[0]], data[columns[1]], data[columns[2]], timeperiod=period)
    minus_di = talib.MINUS_DI(data[columns[0]], data[columns[1]], data[columns[2]], timeperiod=period)

    result = pd.DataFrame({
        'ADX': adx,
        '+DI': plus_di,
        '-DI': minus_di
    })


    if signal:
        signal = []
        for i in range(1, len(result)):
            if result['ADX'].iloc[i] > 25 \
                and result['+DI'].iloc[i-1] <= result['-DI'].iloc[i-1] \
                and result['+DI'].iloc[i] > result['-DI'].iloc[i]:
                    result.loc[result.index[i], 'Signal'] = 1
            elif result['ADX'].iloc[i] > 25 \
                and result['+DI'].iloc[i-1] >= result['-DI'].iloc[i-1] \
                and result['+DI'].iloc[i] < result['-DI'].iloc[i]:
                    result.loc[result.index[i], 'Signal'] = -1
            else:
                result.loc[result.index[i], 'Signal'] = 0

    return result

# ADX, OBV, RSI