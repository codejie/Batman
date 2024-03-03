"""
适配器常量定义
"""

from pandas import DataFrame
# from typing import Dict

StandardTitle = ['Date', 'Time', 'Datetime', 'Symbol', 'Open', 'Close', 'High', 'Low', 'Volume', 'Turnover', 'Volatility', 'Percentage', 'Amount', 'Rate']
AKShareTitle = ['日期', '时间', '日期时间', '代码', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']

def columns_akshare2standard(cols: DataFrame.columns) -> dict:
    ret = dict()
    for col in cols:
        try:
            ret[col] = StandardTitle[AKShareTitle.index(col)]
        except:
            ret[col] = col
    return ret

def columns_standard2akshare(cols: DataFrame.columns) -> dict:
    ret = dict()
    for col in cols:
        try:
            ret[col] = AKShareTitle[StandardTitle.index(col)]
        except:
            ret[col] = col
    return ret

def df_akshare2standard(df: DataFrame) -> DataFrame:
    return df.rename(columns=columns_akshare2standard(df.columns))

def df_standard2akshare(df: DataFrame) -> DataFrame:
    return df.rename(columns=columns_standard2akshare(df.columns))