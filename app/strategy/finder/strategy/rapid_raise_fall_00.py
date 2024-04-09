"""
RapidRaiseFall00FinderStrategy base FS1
全部A股计算Close/Open最近速涨速跌
"""

from datetime import datetime, timedelta
from pandas import DataFrame
from app import logger
from app.strategy.finder.algorithm.fs_1 import FS1Algorithem, FS1Result

from app.task_manager import taskManager
from app.data import stock


class RapidRaiseFall00Strategy:
    _name = '速涨急跌'
    _desc = '全部A股计算Close/Open最近速涨速跌'
    _algorithm = FS1Algorithem

    @staticmethod
    def func(**kwargs):
        logger.debug('RapidRaiseFall00Function:func() called.')
        begin = datetime.now()

        id = kwargs['id']
        response = RapidRaiseFall00Strategy.exec(kwargs)

        taskManager.set_result(id=id, result=response, duration=(datetime.now() - begin))        
        logger.debug('RapidRaiseFall00FinderStrategy:func() end.')

    @staticmethod
    def exec(kwargs: dict) -> dict:
        symbol = kwargs['symbol'] if 'symbol' in kwargs else None
        up_count = int(kwargs['up_count'])
        up_rate = float(kwargs['up_rate']) / 100
        down_count = int(kwargs['down_count'])
        down_rate = float(kwargs['down_rate']) / 100

        start = (datetime.today() - timedelta(30)).strftime('%Y-%m-%d')
        end = datetime.today().strftime('%Y-%m-%d')

        response:dict = {
            'items': []
        }

        codes = stock.get_a_list() if symbol is None else DataFrame.from_dict(symbol)
        for i,r in codes.iterrows():
            df = stock.get_history(r['code'], start, end)
            if df is not None and {'开盘','收盘'}.issubset(df.columns):
                df = df.tail(up_count + down_count).reset_index()
                strategy = FS1Algorithem()
                strategy.load(close=df['收盘'], open=df['开盘'], up_count=up_count, up_rate=up_rate, down_count=down_count, down_rate=down_rate)
                result: FS1Result = strategy.run()
                if result.index and len(result.index) > 0:
                    response['items'].append({
                        'code': r['code'],
                        'name': r['name'],
                        'range': f'{df['日期'].iloc[0]}~{df['日期'].iloc[-1]}',
                        'index': result.index
                    })

        return response   