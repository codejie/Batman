"""
TestStrategy
"""
from datetime import datetime
from app import logger
from app.strategy.finder.algorithm.t_1 import T1Algorithem

from app.task import taskManager

class TestStrategy:
    _name = 'Test'
    _desc = 'for test'
    _algorithm = T1Algorithem 

    @staticmethod
    def func(**kwargs):
        logger.debug('TestFunction:func() called.')
        # logger.debug(kwargs)
        begin = datetime.now()
        id=kwargs['id']
        response = {
            'items': [],
            'updated': datetime.now(),
            'duration': f'{(datetime.now() - begin)}' # '{datetime.now().strftime('%Y%m%d %H%M%S')}({datetime.now() - begin})'
            # 'id': id,
            # 'kwargs': utils.kwargString(kwargs)
        }
        response['items'].append({
            'code': '000001',
            'name': '平安银行',
            'range': '2024-01-01~2024-01-02',
            'index': 1
        })
        # response = TestStrategyResponse(id=id, kwargs=utils.kwargString(kwargs))
        # print(response)
        # instance.set_response(id=id, response=response)
        taskManager.set_result(id=id, result=response, duration=(datetime.now() - begin))        
        logger.debug('TestFunction:func() called end.')
