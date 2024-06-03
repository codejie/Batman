"""
算法类
"""
from abc import ABCMeta, abstractmethod
from typing import Callable, TypeAlias
from app.exception import AppException

class AlgorithmException(AppException):
    def __init__(self, e: Exception) -> None:
        super().__init__(e)

    def __init__(self, message: str) -> None:
        super().__init__(message)

class Argument:
    name: str
    type: str
    unit: str | None = None
    desc: str | None = None
    default: any | None = None
    required: bool = False

class Data:
    name: str
    desc: str

class Result:
    name: str
    desc: str

AlgorithmCallback: TypeAlias = Callable[..., bool]

class Algorithm(ABCMeta):
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

    def set_args(self, **kwargs) -> None:
        for arg in self.args:
            if arg.name in kwargs:
                self.arg_values[arg.name] = kwargs[arg.name]
            elif not arg.required:
                self.arg_values[arg.name] = arg.default
            else:
                raise AlgorithmException(f'{self.name} missing argument {arg.name}')

    def set_data(self, **kwargs) -> None:
        for data in self.data:
            if data.name in kwargs:
                self.data_values[data.name] = kwargs[data.name]
            else:
                raise AlgorithmException(f'{self.name} missing data {data.name}')

    def set_hit(self, callback: AlgorithmCallback) -> None:
        self.callback = callback

    def run(self, start: int = 0) -> None:
        self.pos = start
        while self.pos < self.size:
            if not self.next():
                break
            self.pos += 1

    @abstractmethod
    def next(self) -> bool:
        pass            