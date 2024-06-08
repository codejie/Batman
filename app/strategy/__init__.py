"""
策略基类
"""

from enum import Enum
from app.exception import AppException
from app.strategy.algorithm import Algorithm



class StrategyException(AppException):
    def __init__(self, e: Exception) -> None:
        super().__init__(e)

    def __init__(self, message: str) -> None:
        super().__init__(message)

class Type(Enum):
    FILTER = 0,
    TRADE = 1

class State(Enum):
    INIT = 0
    READY = 1
    RUNNING = 2

class Argument:
    def __init__(self, name: str, type: str, unit: str = None, desc: str = None, default: any = None, required: bool = True) -> None:
        self.name = name
        self.type = type
        self.unit = unit
        self.desc = desc
        self.default = default
        self.required = required

class Data:
    def __init__(self, name: str, type: str, desc: str = None) -> None:
        self.name = name
        self.type = type
        self.desc = desc

class Strategy:
    type: Type
    name: str
    desc: str
    args: list[Argument] = []
    data: list[Data] = []
    algorithms: list[Algorithm] = []

    def __init__(self) -> None:
        self.state = State.READY

    def set_args(self, values: dict) -> None:
        for arg in self.args:
            if arg.name in values:
                self.arg_values[arg.name] = values[arg.name]
            elif not arg.required:
                self.arg_values[arg.name] = arg.default
            else:
                raise StrategyException(f'{self.name} missing argument {arg.name}')

    def set_data(self, values: dict) -> None:
        for data in self.data:
            if data.name in values:
                self.data_values[data.name] = values[data.name]
            else:
                raise StrategyException(f'{self.name} missing data {data.name}')
    
    def set_id(self, id: str) -> None:
        self.id = id

