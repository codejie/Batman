"""
策略基类
"""
from enum import Enum
from app.exception import AppException
from app.strategy.algorithm import Algorithm

class AppException(AppException):
    def __init__(self, e: Exception) -> None:
        super().__init__(e)

    def __init__(self, message: str) -> None:
        super().__init__(message)

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
    
class Result:
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
    results: list[Result] = None
    
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
    RUNNING = 2
    PAUSED = 3

class StrategyInstance:
    def __init__(self, id: str, name: str, strategy: str, trigger: dict) -> None:
        self.id: str = id
        self.name: str = name
        self.strategy: str = strategy # strategy.id
        self.trigger: dict = trigger

        self.state = State.READY
        self.arg_values: dict = {}
        self.algo_values: dict[str, dict] = {}

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
            vs = algo_values[algorithm.name] if algorithm.name in algo_values else {}
            for args in algorithm.args:
                if (not (args.name in vs)) and args.required:
                    raise AppException(f'algorithm \'{algorithm.name}\' missing argument \'{args.name}\'')

        # self.algo_values = algo_values # todo: check algorithm args

    def set_trigger(self, trigger:dict) -> None:
        self.trigger = trigger

    def set_state(self, state: State) -> None:
        self.state = state

    def get_func() -> callable:
        pass
