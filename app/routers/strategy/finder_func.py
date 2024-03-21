"""
策略方法定义
"""
from pydantic import BaseModel
from datetime import datetime, timedelta
from pandas import DataFrame

from app import AppException, logger

from app.data import stock
from app.strategy.finder.fs_1 import FS1Result, FS1Strategy
from app.routers import utils

"""
策略列表
"""

"""
Strategy Response
"""
class FS1StrategyResponse(BaseModel):
    updated: str = ''
    items: list[dict] = []

class FinderStrategyFunction:

    _fs1Response: FS1StrategyResponse = FS1StrategyResponse()

    @staticmethod
    def get(name: str) -> callable:
        if name == 'fs1':
            return FinderStrategyFunction.funcFinderFS1
        else:
            raise AppException(f'not found strategy - {name}')
    
    @staticmethod
    def funcFinderFS1(**kwargs):
        logger.info('funcFinderFS1() called.')

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

        FinderStrategyFunction._fs1Response.items.clear()

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
                    FinderStrategyFunction._fs1Response.items.append({
                        'code': r['code'],
                        'name': r['name'],
                        'range': f'{df['日期'].iloc[0]} - {df['日期'].iloc[-1]}',
                        'index': result.index
                    })
                    
        FinderStrategyFunction._fs1Response.updated = f'{datetime.today().strftime('%Y%m%d')}({datetime.now() - begin})'

        # print(FinderStrategyFunction._fs1Response)