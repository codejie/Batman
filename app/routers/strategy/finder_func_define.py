"""
策略函数相关定义
"""
from app import AppException
from app.routers.strategy.finder_func import TestStrategy, RapidRaiseFall00FinderStrategy

class StrategyInfo:
    name: str
    desc: str
    args: list

class StrategyFuncInfo:
    name: str
    desc: str
    func: callable
    strategy: StrategyInfo

"""
策略函数列表
"""
finderStrategyFuncList: dict[str, dict] = {
    'Test': {
        'name': TestStrategy._name,
        'desc': TestStrategy._desc,
        'func': TestStrategy.func,
        'strategy': TestStrategy._strategy
    },
    'RapidRaiseFall00FinderStrategy': {
        'name': RapidRaiseFall00FinderStrategy._name,
        'desc': RapidRaiseFall00FinderStrategy._desc,
        'func': RapidRaiseFall00FinderStrategy.func,
        'strategy': RapidRaiseFall00FinderStrategy._strategy
    }
} 

def getFinderStrategyFunc(name: str | None = None) -> dict | list[dict] | None:
    if name is None:
        return finderStrategyFuncList
    else:
        return finderStrategyFuncList[name]

def validFinderStrategyFunc(name: str, kwargs: dict) -> dict | None:
    func = finderStrategyFuncList[name]
    if func is None:
        return None
    
    strategy = func['strategy']
    if strategy is None and strategy['args'] is None:
        raise AppException(code=-1, message=f'strategy \'{strategy['name']}\' not found')
    args = strategy['args']
    for arg in args:
        if arg['name'] not in kwargs:
            if 'default' not in arg:
                raise AppException(code=-100, message=f'strategy \'{strategy['name']}\' missing argument \'{arg['name']}\'')
            else:
                kwargs[arg['name']] = arg['default']
    return func
