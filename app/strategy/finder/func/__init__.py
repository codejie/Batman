"""
策略函数相关定义
"""
from datetime import datetime, timedelta
from app import AppException
from app.strategy.finder.func import func

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

def addStrategyFuncList(strategy: callable):
    finderStrategyFuncList[strategy._name] = strategy

finderStrategyFuncList: dict[str, callable] = {}

addStrategyFuncList(func.TestFunction)
addStrategyFuncList(func.RapidRaiseFall00Function)
addStrategyFuncList(func.HSGTRaise00StrategyFunction)
addStrategyFuncList(func.MarginRaise00StrategyFunction)

# print(f'funlist = \n{finderStrategyFuncList}')

def getFinderStrategyFunc(name: str) -> callable:
    return finderStrategyFuncList.get(name, None)
    
def getFinderStrategyFuncList() -> dict:
    return finderStrategyFuncList

def validFinderStrategyFunc(name: str, kwargs: dict) -> callable:
    strategyFunc = finderStrategyFuncList.get(name, None)
    if strategyFunc is None:
        return None
    
    strategy = strategyFunc._strategy
    if strategy is None:
        raise AppException(code=-1, message=f'strategy \'{strategy._name}\' not found')
    args = strategy._args
    for arg in args:
        if arg['name'] not in kwargs:
            if 'default' not in arg:
                raise AppException(code=-100, message=f'strategy \'{strategy._name}\' missing argument \'{arg['name']}\'')
            else:
                kwargs[arg['name']] = arg['default']
    return strategyFunc
