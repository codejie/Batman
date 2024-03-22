"""
策略方法定义
"""
from pydantic import BaseModel
from datetime import datetime, timedelta
from pandas import DataFrame

from app import AppException, logger

from app.data import stock
from app.strategy.finder.fs_1 import FS1Result, FS1Strategy
from app.strategy.finder.t_1 import T1Strategy
from app.routers import utils

class FinderStrategyResponse(BaseModel):
    updated: str = ''

"""
TestStrategy
"""
class TestStrategy:
    _name = 'TestStrategy'
    _desc = 'for test'
    _strategy = {
        'name': T1Strategy._name,
        'desc': T1Strategy._desc,
        'args': T1Strategy._args
    }

    @staticmethod
    def func(**kwargs):
        logger.debug('TestStrategy:func() called')
        logger.debug(kwargs)

"""
RapidRaiseFall00FinderStrategy base FS1
全部A股计算Close/Open最近速涨速跌
"""
class RapidRaiseFall00FinderStrategyResponse(FinderStrategyResponse):
    items: list[dict] = []

class RapidRaiseFall00FinderStrategy:
    _name = 'RapidRaiseFall00FinderStrategy'
    _desc = '全部A股计算Close/Open最近速涨速跌'
    _strategy = {
        'name': FS1Strategy._name,
        'desc': FS1Strategy._desc,
        'args': FS1Strategy._args
    }

    _response: RapidRaiseFall00FinderStrategyResponse = RapidRaiseFall00FinderStrategyResponse()

    @staticmethod
    def func(**kwargs):
        logger.info('RapidRaiseFall00FinderStrategy:func() called.')

        begin = datetime.now()
        symbol = kwargs['symbol']
        # start = utils.dateConvert1(kwargs['start'])
        # end = utils.dateConvert1(kwargs['end'])
        up_count = int(kwargs['up_count'])
        up_rate = float(kwargs['up_rate']) / 100
        down_count = int(kwargs['down_count'])
        down_rate = float(kwargs['down_rate']) / 100

        start = (datetime.today() - timedelta(30)).strftime('%Y%m%d')
        end = datetime.today().strftime('%Y%m%d')

        RapidRaiseFall00FinderStrategy._response.items.clear()

        codes = DataFrame()
        if 'symbol' in kwargs:
            codes = codes.from_dict(kwargs['symbol'])
            print(codes)
        else:
            codes = stock.get_a_code()

        for i,r in codes.iterrows():
            df = stock.get_history(r['code'], start, end)
            if df is not None and {'开盘','收盘'}.issubset(df.columns):
                df = df.tail(up_count + down_count).reset_index()
                # print(df)
                strategy = FS1Strategy()
                print(f'{r['code']} - {up_count} {up_rate} {down_count} {down_rate} -- {len(df)}')
                strategy.load(close=df['收盘'], open=df['开盘'], up_count=up_count, up_rate=up_rate, down_count=down_count, down_rate=down_rate)
                result: FS1Result = strategy.run()
                print(result)
                if result.index and len(result.index) > 0:
                    RapidRaiseFall00FinderStrategy._response.items.append({
                        'code': r['code'],
                        'name': r['name'],
                        'range': f'{df['日期'].iloc[0]} - {df['日期'].iloc[-1]}',
                        'index': result.index
                    })
                    
        RapidRaiseFall00FinderStrategy._response.updated = f'{datetime.today().strftime('%Y%m%d')}({datetime.now() - begin})'
