"""
Test Strategy
"""

from app.strategy.finder import FinderResult, FinderStrategy

from app import logger

class T1Strategy(FinderStrategy):
    _name = 't1'
    _desc = 'for test'
    _args = [
        {
            'name': 'a',
            'type': 'string',
            'unit': '',
            'desc': 'argument a',
            'default': 'none'
        }
    ]

    def __init__(self):
        super().__init__(self.name, self._desc)

    def load(self, **kwargs) -> bool:
        logger.debug('T1Strategy:load()')
        return super().load(kwargs)
    
    def _update(self) -> bool:
        logger.debug('T1Strategy:update()')
        return super()._update()
    
    def _next(self) -> bool:
        logger.debug('T1Strategy:_next()')
        return True