"""
FinderStrategy Base Classes
"""

from app.strategy import Result, Strategy, Type

class FinderResult(Result):

    def __init__(self) -> None:
        super().__init__()
        self.index = []

    def represent(self, **kwargs) -> str:
        return str(self.index)

class FinderStrategy(Strategy):
    def __init__(self, name: str = 'undefined', desc: str | None = None):
        super().__init__(Type.Finder, name, desc)
 