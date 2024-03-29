"""
策略方法定义
"""
from datetime import datetime, timedelta
from pandas import DataFrame
from pydantic import BaseModel

from app import AppException, logger

from app.data import stock
from app.strategy.finder.fs_1 import FS1Result, FS1Strategy
from app.strategy.finder.t_1 import T1Strategy
from app.routers import utils
from app.routers.strategy.local_cache import setFinderStrategyInstanceResponse
# from app.routers.strategy.finder_model import FinderStrategyResponse
# class FinderStrategyResponse(BaseModel):
#     updated: str = ''

"""
TestStrategy
"""
# class TestStrategyResponse(FinderStrategyResponse):
#     id: str
#     kwargs: str

class TestStrategy:
    _name = 'Test'
    _desc = 'for test'
    _strategy = {
        'name': T1Strategy._name,
        'desc': T1Strategy._desc,
        'args': T1Strategy._args
    }
    # _response: TestStrategyResponse | None = None

    @staticmethod
    def func(**kwargs):
        logger.debug('TestStrategy:func() called')
        logger.debug(kwargs)
        id=kwargs['id']
        response = {
            'updated': f'{datetime.today().strftime('%Y%m%d')}',
            'id': id,
            'kwargs': utils.kwargString(kwargs)
        }
        # response = TestStrategyResponse(id=id, kwargs=utils.kwargString(kwargs))
        # print(response)
        setFinderStrategyInstanceResponse(id=id, response=response)


"""
RapidRaiseFall00FinderStrategy base FS1
全部A股计算Close/Open最近速涨速跌
"""
# class RapidRaiseFall00FinderStrategyResponse(FinderStrategyResponse):
#     items: list[dict] = []

class RapidRaiseFall00FinderStrategy:
    _name = '速涨急跌'
    _desc = '全部A股计算Close/Open最近速涨速跌'
    _strategy = {
        'name': FS1Strategy._name,
        'desc': FS1Strategy._desc,
        'args': FS1Strategy._args
    }

    # _response: RapidRaiseFall00FinderStrategyResponse = RapidRaiseFall00FinderStrategyResponse()

    @staticmethod
    def func(**kwargs):
        logger.debug('RapidRaiseFall00FinderStrategy:func() called.')
        id = kwargs['id']
        # start = utils.dateConvert1(kwargs['start'])
        # end = utils.dateConvert1(kwargs['end'])
        up_count = int(kwargs['up_count'])
        up_rate = float(kwargs['up_rate']) / 100
        down_count = int(kwargs['down_count'])
        down_rate = float(kwargs['down_rate']) / 100

        start = (datetime.today() - timedelta(30)).strftime('%Y%m%d')
        end = datetime.today().strftime('%Y%m%d')

        response:dict = {
            'items': []
        }

        # RapidRaiseFall00FinderStrategy._response.items.clear()
        begin = datetime.now()
        codes = DataFrame()
        if 'symbol' in kwargs:
            codes = codes.from_dict(kwargs['symbol'])
            # print(codes)
        else:
            codes = stock.get_a_code()

        for i,r in codes.iterrows():
            df = stock.get_history(r['code'], start, end)
            if df is not None and {'开盘','收盘'}.issubset(df.columns):
                df = df.tail(up_count + down_count).reset_index()
                strategy = FS1Strategy()
                strategy.load(close=df['收盘'], open=df['开盘'], up_count=up_count, up_rate=up_rate, down_count=down_count, down_rate=down_rate)
                result: FS1Result = strategy.run()
                if result.index and len(result.index) > 0:
                    # RapidRaiseFall00FinderStrategy._response.items.append({
                    response['items'].append({
                        'code': r['code'],
                        'name': r['name'],
                        'range': f'{df['日期'].iloc[0]} - {df['日期'].iloc[-1]}',
                        'index': result.index
                    })
                    
        # RapidRaiseFall00FinderStrategy._response.updated = f'{datetime.today().strftime('%Y%m%d')}({datetime.now() - begin})'
        response['updated'] = f'{datetime.today().strftime('%Y%m%d %H%M%S')}({datetime.now() - begin})'
        setFinderStrategyInstanceResponse(id=id, response=response)

        logger.debug('RapidRaiseFall00FinderStrategy:func() end.')
