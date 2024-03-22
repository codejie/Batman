"""
策略方法定义
"""
from pydantic import BaseModel

from app import AppException, logger

from app.data import stock
from app.strategy.finder.fs_1 import FS1Result, FS1Strategy
from app.routers import utils

"""
Strategy Response
"""
class FS1StrategyResponse(BaseModel):
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
        logger.debug("====================fs1")
        logger.debug(kwargs)
        symbol = kwargs['symbol']
        start = utils.dateConvert1(kwargs['start'])
        end = utils.dateConvert1(kwargs['end'])
        up_count = int(kwargs['up_count'])
        up_rate = float(kwargs['up_rate']) / 100
        down_count = int(kwargs['down_count'])
        down_rate = float(kwargs['down_rate']) / 100

        df = stock.get_history(symbol[0], start, end)
        print(df)
        strategy = FS1Strategy()
        strategy.load(close=df['收盘'], open=df['开盘'], up_count=up_count, up_rate=up_rate, down_count=down_count, down_rate=down_rate)
        result: FS1Result = strategy.run()

        # if result.index and len(result.index) > 0:
        FinderStrategyFunction._fs1Response.items.clear()
        FinderStrategyFunction._fs1Response.items.append({
            'code': symbol[0],
            'index': result.index
        })

        print(FinderStrategyFunction._fs1Response)