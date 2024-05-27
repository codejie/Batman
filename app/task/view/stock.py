"""
股票数据视图加工函数
"""
from datetime import datetime

from app.data import stock
from app import utils

"""
股票每日数据
"""
def view_daily_history(**kwargs):
    # today = kwargs['today']
    today = utils.date2String2(datetime.now())

    symbols = stock.get_a_list()

    for index, row in symbols.iterrows():
        pass