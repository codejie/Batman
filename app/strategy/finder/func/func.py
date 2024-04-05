"""
策略方法定义
"""
from datetime import datetime, timedelta
from pandas import DataFrame

from app import AppException, logger

from app.data import stock
from app.strategy.finder import FinderStrategy, FinderResult
from app.strategy.finder.base.fs_1 import FS1Strategy, FS1Result
from app.strategy.finder.base.fs_2 import FS2Strategy, FS2Result
from app.strategy.finder.base.t_1 import T1Strategy
from app.routers import utils
from app.strategy.finder.func.local_cache import setFinderStrategyInstanceResponse

"""
Finder Strategy Function Base
"""
class FinderStrategyFunction:

    @staticmethod
    def bindStrategy(base: FinderStrategy) -> dict:
        return {
            'name': base._name,
            'desc': base._desc,
            'args': base._args
        }

"""
TestStrategy
"""
# class TestStrategyResponse(FinderStrategyResponse):
#     id: str
#     kwargs: str

class TestFunction(FinderStrategyFunction):
    _name = 'Test'
    _desc = 'for test'
    _strategy = FinderStrategyFunction.bindStrategy(T1Strategy)

    @staticmethod
    def func(**kwargs):
        logger.debug('TestStrategy:func() called')
        # logger.debug(kwargs)
        begin = datetime.now()
        id=kwargs['id']
        response = {
            'items': [],
            'updated': datetime.now(),
            'duration': f'{(datetime.now() - begin)}' # '{datetime.now().strftime('%Y%m%d %H%M%S')}({datetime.now() - begin})'
            # 'id': id,
            # 'kwargs': utils.kwargString(kwargs)
        }
        response['items'].append({
            'code': '000001',
            'name': '平安银行',
            'range': '2024-01-01~2024-01-02',
            'index': 1
        })
        # response = TestStrategyResponse(id=id, kwargs=utils.kwargString(kwargs))
        # print(response)
        setFinderStrategyInstanceResponse(id=id, response=response)


"""
RapidRaiseFall00FinderStrategy base FS1
全部A股计算Close/Open最近速涨速跌
"""
# class RapidRaiseFall00FinderStrategyResponse(FinderStrategyResponse):
#     items: list[dict] = []

class RapidRaiseFall00Function(FinderStrategyFunction):
    _name = '速涨急跌'
    _desc = '全部A股计算Close/Open最近速涨速跌'
    _strategy = FinderStrategyFunction.bindStrategy(FS1Strategy)

    @staticmethod
    def func(**kwargs):
        logger.debug('RapidRaiseFall00Function:func() called.')
        id = kwargs['id']
        # start = utils.dateConvert1(kwargs['start'])
        # end = utils.dateConvert1(kwargs['end'])
        up_count = int(kwargs['up_count'])
        up_rate = float(kwargs['up_rate']) / 100
        down_count = int(kwargs['down_count'])
        down_rate = float(kwargs['down_rate']) / 100

        start = (datetime.today() - timedelta(30)).strftime('%Y-%m-%d')
        end = datetime.today().strftime('%Y-%m-%d')

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
            codes = stock.get_a_list()

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
                        'range': f'{df['日期'].iloc[0]}~{df['日期'].iloc[-1]}',
                        'index': result.index
                    })
                    
        # RapidRaiseFall00FinderStrategy._response.updated = f'{datetime.today().strftime('%Y%m%d')}({datetime.now() - begin})'
        response['updated'] =  datetime.now() # f'{datetime.now().strftime('%Y%m%d %H%M%S')}({datetime.now() - begin})'
        response['duration'] = f'{(datetime.now() - begin)}'

        setFinderStrategyInstanceResponse(id=id, response=response)
        logger.debug('RapidRaiseFall00FinderStrategy:func() end.')

"""
HSGTRaise00StrategyFunction
全部股票连续持股数量(hsgt)变化
"""
class HSGTRaise00StrategyFunction(FinderStrategyFunction):
    _name = '北向持股数量变化'
    _desc = '全部股票连续北向持股数量(hsgt)变化'
    _strategy = FinderStrategyFunction.bindStrategy(FS2Strategy)

    @staticmethod
    def func(**kwargs):
        begin = datetime.now()
        logger.debug('HSGTRaise00StrategyFunction:func() called.')

        id = kwargs['id']
        symbol = kwargs['symbol'] if 'symbol' in kwargs else None
        days = int(kwargs['days'])
        rate = float(kwargs['rate']) / 100

        start = (datetime.today() - timedelta(15)).strftime('%Y-%m-%d')
        end = datetime.today().strftime('%Y-%m-%d')

        response: dict = {
            'items': []
        }

        codes = stock.get_a_list() if symbol is None else DataFrame({ 'code': [kwargs['symbol']], 'name': [''] })
        for index, row in codes.iterrows():
            df = None
            try:
                df = stock.get_hsgt(row['code'], start, end)
            except:
                logger.warn(f'{row['code']} hsgt data is None.')
                continue

            if df is not None and {'持股数量'}.issubset(df.columns):
                df = df.tail(days).reset_index()
                # print(df)
                strategy = FS2Strategy()
                strategy.load(data=df['持股数量'], days=days, rate=rate)
                result: FS2Result = strategy.run()
                if result.index and len(result.index) > 0:
                    response['items'].append({
                        'code': row['code'],
                        'name': row['name'],
                        'range': f'{df['持股日期'].iloc[0]}~{df['持股日期'].iloc[-1]}',
                        'index': result.index
                    })
        response['updated'] =  datetime.now()
        response['duration'] = f'{(datetime.now() - begin)}'

        setFinderStrategyInstanceResponse(id=id, response=response)
        logger.debug('HSGTRaise00StrategyFunction:func() end.')                


"""
MarginRaise00StrategyFunction
全部股票连续融资余额变化
"""
class MarginRaise00StrategyFunction(FinderStrategyFunction):
    _name = '融资余额变化'
    _desc = '全部股票连续融资余额(margin)变化'
    _strategy = FinderStrategyFunction.bindStrategy(FS2Strategy)

    @staticmethod
    def func(**kwargs):
        begin = datetime.now()
        logger.debug('MarginRaise00StrategyFunction:func() called.')

        id = kwargs['id']
        symbol = kwargs['symbol'] if 'symbol' in kwargs else None
        days = int(kwargs['days'])
        rate = float(kwargs['rate']) / 100

        start = (datetime.today() - timedelta(15)).strftime('%Y-%m-%d')
        end = datetime.today().strftime('%Y-%m-%d')

        response: dict = {
            'items': []
        }

        codes = stock.get_a_list() if symbol is None else DataFrame({ 'code': [kwargs['symbol']], 'name': [''] })
        for index, row in codes.iterrows():
            df = None
            try:
                df = stock.get_margin(row['code'], start, end)
            except:
                logger.warn(f'{row['code']} margin data is None.')
                continue

            if df is not None and {'融资余额'}.issubset(df.columns):
                df = df.tail(days).reset_index()
                # print(df)
                strategy = FS2Strategy()
                strategy.load(data=df['融资余额'], days=days, rate=rate)
                result: FS2Result = strategy.run()
                if result.index and len(result.index) > 0:
                    response['items'].append({
                        'code': row['code'],
                        'name': row['name'],
                        'range': f'{df['日期'].iloc[0]}~{df['日期'].iloc[-1]}',
                        'index': result.index
                    })
        response['updated'] =  datetime.now()
        response['duration'] = f'{(datetime.now() - begin)}'

        setFinderStrategyInstanceResponse(id=id, response=response)
        logger.debug('MarginRaise00StrategyFunction:func() end.')

