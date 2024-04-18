"""
Finder算法类定义
"""

from abc import ABCMeta, abstractmethod

class Result:
    def __init__(self) -> None:
        self.index = []

    def represent(self, **kwargs) -> str:
        return str(self.index)
    
class Algorithm(metaclass=ABCMeta):
    def __init__(self, name: str, desc: str | None = None):
        self.name = name
        self.desc = desc

        self.size = -1
        self.pos = -1
        self.result = None
    
    def run(self, start: int = 0) -> Result:
        self.pos = start
        while self.pos < self.size:
            if not self.next():
                break
            self.pos += 1
        return self.result
    
    def __repr__(self) -> str:
        return f'<{self.type.name}>[{self.name}]:{self.desc}\n{super().__repr__()}'

    def load(self, **kwargs) -> bool:
        return self.update()

    @abstractmethod
    def update(self) -> bool:
        """
        Must call after load(), used to init some inner variants, such as Size
        """
        return True

    @abstractmethod
    def next(self) -> bool:
        pass
    