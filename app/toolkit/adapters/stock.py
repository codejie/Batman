"""
股票数据转换函数集合，标准化处理数据，以分析工具所需为主
"""

from pandas import DataFrame
from ... import AppException
from ...datasource import DataSource, stock

# StandardTitle = ['Date', 'Time', 'Datetime', 'Symbol', 'Open', 'Close', 'High', 'Low', 'Volume', 'Turnover', 'Volatility', 'Percentage', 'Amount', 'Rate']
# AKShareTitle = ['日期', '时间', '日期时间', '代码', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率']

def history( src: DataFrame | None, ds: DataSource = stock.DATA_SOURCE) -> DataFrame:
    if src is None: return None
    src.columns.values
    if ds == DataSource.AKSHARE:
        return src.rename(columns={
            '日期': 'Date',
            '开盘': 'Open',
            '收盘': 'Close',
            '最高': 'High',
            '最低': 'Low',
            '成交量': 'Volume',
            '成交额': 'Turnover',
            '振幅': 'Volatility',
            '涨跌幅': 'Percentage ',
            '涨跌额': 'Amount',
            '换手率': 'Rate'
        })
    else:
        raise AppException(-1, f'unknown data source - {ds.name}')