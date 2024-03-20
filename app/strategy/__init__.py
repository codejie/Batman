"""
策略类定义
"""

from enum import Enum
from abc import ABCMeta, abstractmethod

class Type(Enum):
    Finder = 0
    Trader = 1

class Result:
    pass

class Strategy(metaclass=ABCMeta):
    def __init__(self, type: Type, name: str, desc: str | None = None):
        self.type = type
        self.name = name
        self.desc = desc

        self._size = -1
        self._pos = -1
        self._result = None
    
    def run(self, start: int = 0) -> Result:
        self._pos = start
        while self._pos < self._size:
            if not self._next():
                break
            self._pos += 1
        return self._result
    
    def __repr__(self) -> str:
        return f'<{self.type.name}>[{self.name}]:{self.desc}\n{super().__repr__()}'

    def load(self, **kwargs) -> bool:
        return self._update()

    @abstractmethod
    def _update(self) -> bool:
        """
        Must call after load(), used to init some inner variants, such as _Size
        """
        return True

    @abstractmethod
    def _next(self) -> bool:
        pass
    