"""
算法类
"""
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Callable, TypeAlias
from app.exception import AppException

class Argument:
    def __init__(self, name: str, type: str, unit: str = None, desc: str = None, value: list[any] = None, default: any = None, required: bool = True) -> None:
        self.name = name
        self.type = type
        self.unit = unit
        self.desc = desc
        self.value = value # option while type is list, { value: any, desc: ''}
        self.default = default
        self.required = required

class Data:
    def __init__(self, name: str, type: str, desc: str = None) -> None:
        self.name = name
        self.type = type
        self.desc = desc

class Result:
    def __init__(self, name: str, type: str, desc: str = None) -> None:
        self.name = name
        self.type = type
        self.desc = desc

"""
callback(event: str, result: dict) -> bool
event:
    - 'start': called while begin to run
        {
            pos: start position,
            size: data size
        }
    - 'hit': called while algorithm hit
        {
            - result struct of algorithm
        }
        such as:
        {
            pos: position of hit
        }
    - 'end': called while process end
        {
            broken: False: process normally exit, True: process be broken to exit
        }
return:
    - True: continue
    - False: break
"""
class CallbackType(Enum):
    START = 'start'
    HIT = 'hit'
    END = 'end'
    
AlgorithmCallback: TypeAlias = Callable[[CallbackType, dict], bool]

class Algorithm(metaclass=ABCMeta):
    name: str = 'Algorithm'
    desc: str = 'Algorithm Base'
    args: list[Argument] = []
    data: list[Data] = []
    results: list[Result] = []

    def __init__(self) -> None:
        self.arg_values = {}
        self.data_values = {}
        self.size = 0
        self.pos = 0
        self.callback = None

    def set_args(self, values: dict) -> None:
        for arg in self.args:
            if arg.name in values:
                self.arg_values[arg.name] = values[arg.name]
            elif not arg.required:
                self.arg_values[arg.name] = arg.default
            else:
                raise AppException(f'{self.name} missing argument {arg.name}')
                    
    def set_data(self, values: dict) -> None:
        for data in self.data:
            if data.name in values:
                self.data_values[data.name] = values[data.name]
            else:
                raise AppException(f'{self.name} missing data {data.name}')

    def set_callback(self, callback: AlgorithmCallback) -> None:
        self.callback = callback

    def run(self, start: int = 0) -> None:
        self.pos = start

        # if self.callback:
        #     self.callback(CallbackType.START, {
        #         'pos': self.pos,
        #         'size': self.size
        #     })

        # broken: bool = False
        while self.pos < self.size:
            if not self.next():
                # broken = True
                break
            self.pos += 1

        # if self.callback:
        #     self.callback(CallbackType.END, {
        #         'broken': broken
        #     })            

    @abstractmethod
    def next(self) -> bool:
        return True            