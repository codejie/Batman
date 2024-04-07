"""
策略函数相关定义
"""

from app import AppException
from app.strategy.finder.strategy.test import TestStrategy
from app.strategy.finder.strategy.rapid_raise_fall_00 import RapidRaiseFall00Strategy
from app.strategy.finder.strategy.hsgt_raise_00 import HSGTRaise00Strategy
from app.strategy.finder.strategy.margin_raise_00 import MarginRaise00Strategy


# class StrategyInfo:
#     name: str
#     desc: str
#     args: list

# class StrategyFuncInfo:
#     name: str
#     desc: str
#     func: callable
#     strategy: StrategyInfo

# class StrategyFuncResultItem:
#     code: str
#     name: str
#     range: str
#     index: int

# class StrategyFuncResponse:
#     _type: int = 0 # response type, 0: base; 1: code & name

#     def __init__(self, t: int) -> None:
#         self._type = t
#         self.items: list[StrategyFuncResultItem] = []
#         self.updated: datetime = None
#         self.duration: timedelta = None


"""
策略函数列表
"""

def add(strategy: callable):
    finderStrategyList[strategy._name] = strategy

def get(name: str) -> callable:
    return finderStrategyList.get(name, None)
    
def getList() -> dict:
    return finderStrategyList

def valid(name: str, kwargs: dict) -> callable:
    strategy = finderStrategyList.get(name, None)
    if strategy is None:
        return None
    
    algorithm = strategy._algorithm
    if strategy is None:
        raise AppException(code=-1, message=f'algorithm \'{algorithm._name}\' not found')
    args = algorithm._args
    for arg in args:
        if arg['name'] not in kwargs:
            if 'default' not in arg:
                raise AppException(code=-100, message=f'algorithm \'{algorithm._name}\' missing argument \'{arg['name']}\'')
            else:
                kwargs[arg['name']] = arg['default']
    return strategy

finderStrategyList: dict[str, callable] = {}

add(TestStrategy)
add(RapidRaiseFall00Strategy)
add(HSGTRaise00Strategy)
add(MarginRaise00Strategy)
