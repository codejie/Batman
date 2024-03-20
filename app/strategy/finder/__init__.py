"""
FinderStrategy Base Classes
"""

from .. import Result, Strategy, Type

class FinderResult(Result):
    index: list[int] = []

    def represent(self, **kwargs) -> str:
        return str(self.index)

class FinderStrategy(Strategy):
    def __init__(self, name: str = 'undefined', desc: str | None = None):
        super().__init__(Type.Finder, name, desc)
