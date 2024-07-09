"""
策略基类
"""
from datetime import datetime
from enum import Enum
from app.exception import AppException
from app.strategy.algorithm import Algorithm

class Type(Enum):
    FILTER: int = 0
    TRADE: int = 1

class Argument:
    def __init__(self, name: str, type: str, unit: str = None, desc: str = None, value:list[dict[str, any]] = None, default: str = None, required: bool = True) -> None:
        self.name = name
        self.type = type
        self.unit = unit
        self.desc = desc
        self.value = value
        self.default = default
        self.required = required
    
class ResultField:
    def __init__(self, name: str, type: str, desc: str = None) -> None:
        self.name = name
        self.type = type
        self.desc = desc    

# class Data:
#     def __init__(self, name: str, type: str, desc: str = None) -> None:
#         self.name = name
#         self.type = type
#         self.desc = desc

class Strategy:
    id: str
    type: Type
    name: str
    desc: str
    args: list[Argument] = None
    algorithms: list[Algorithm] = None
    result_fields: list[ResultField] = None
    
    @staticmethod
    def func(**kwargs) -> None:
        """
            kwargs:
                - id: instance id
                - values: strategy arg values
                - algo_values: argorithms' args values
        """
        pass

"""
Strategy Instance
"""
class State(Enum):
    INIT = 0
    READY = 1
    EXECUTED = 2
    ERROR = 3
    MISSED = 4
    REMOVED = 5
    PAUSED = 6

class StrategyInstance:
    def __init__(self, type: Type, id: str, name: str, strategy: str, trigger: dict) -> None:
        self.type = type
        self.id: str = id
        self.name: str = name
        self.strategy: str = strategy # strategy.id
        self.trigger: dict = trigger

        self.arg_values: dict = {}
        self.algo_values: dict[str, dict] = {}
        self.results: list = None
        self.latest_updated: datetime = None
        self.run_times = 0
        
        self.state = State.READY
        self.is_removed = False


    def set_args(self, strategy: Strategy, values: dict, algo_values: dict[str, dict] | None = None) -> None:
        args = strategy.args
        for arg in args:
            if arg.name in values:
                self.arg_values[arg.name] = values[arg.name]
            elif not arg.required:
                self.arg_values[arg.name] = arg.default
            else:
                raise AppException(f'strategy \'{self.name}\' missing argument \'{arg.name}\'')
        for algorithm in strategy.algorithms:
            self.algo_values[algorithm.name] = {}
            vs = algo_values[algorithm.name] if algorithm.name in algo_values else {}
            for arg in algorithm.args:
                if arg.name in vs:
                    self.algo_values[algorithm.name][arg.name] = vs[arg.name]
                elif not arg.required:
                    self.algo_values[algorithm.name][arg.name] = arg.default
                else:
                    raise AppException(f'algorithm \'{algorithm.name}\' missing argument \'{args.name}\'')

        # self.algo_values = algo_values # todo: check algorithm args

    def set_trigger(self, trigger:dict) -> None:
        self.trigger = trigger

    def set_state(self, state: State) -> None:
        if state == State.REMOVED:
            self.is_removed = True
        if not self.is_removed:
            self.state = state

    def set_removed(self, removed: bool) -> None:
        self.is_removed = removed

    def get_func() -> callable:
        pass
