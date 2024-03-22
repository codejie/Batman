"""
策略函数相关定义
"""

from pydantic import BaseModel

from app.routers.strategy.finder_func import RapidRaiseFall00FinderStrategy

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
    'RapidRaiseFall00FinderStrategy': {
        'name': RapidRaiseFall00FinderStrategy._name,
        'desc': RapidRaiseFall00FinderStrategy._desc,
        'func': RapidRaiseFall00FinderStrategy.func,
        'strategy': RapidRaiseFall00FinderStrategy._strategy
    }
} 

