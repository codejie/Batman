"""
适配器常量定义
"""

from pandas import DataFrame
# from typing import Dict

StandardTitle = ['Date', 'Time', 'Datetime', 'Symbol', 'Open', 'Close', 'High', 'Low', 'Volume', 'Turnover', 'Volatility', 'Percentage', 'Amount', 'Rate', 'Date', 'Close', 'Percentage', 'Number', 'Value', 'Held_in_A_Shares', 'Value_Change_1', 'Value_Change_5', 'Value_Change_10']
AKShareTitle = ['日期', '时间', '日期时间', '代码', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率', '持股日期', '当日收盘价', '当日涨跌幅', '持股数量', '持股市值', '持股数量占A股百分比', '持股市值变化-1日', '持股市值变化-5日', '持股市值变化-10日']

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