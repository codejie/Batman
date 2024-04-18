"""
Test Algorithm
"""

from app.strategy.finder.algorithm import Algorithm, Result

from app import logger

class T1Algorithem(Algorithm):
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
    
    def update(self) -> bool:
        logger.debug('T1Strategy:update()')
        return super().update()
    
    def next(self) -> bool:
        logger.debug('T1Strategy:_next()')
        return True