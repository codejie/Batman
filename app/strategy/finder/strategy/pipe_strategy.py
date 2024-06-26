"""
策略组合函数
"""
from pandas import DataFrame
from datetime import datetime
from app.data import stock
from app import logger

from app.strategy.finder import strategy
from app.task_manager import taskManager
# symbol
# strategy
# args

def PipeStrategyFunction(**kwargs) -> None:
    logger.debug('PipeStrategyFunction() called.')
    # print(kwargs)
    begin = datetime.now()
    id = kwargs['id']
    symbol = kwargs['symbol'] if 'symbol' in kwargs else None
    codes = stock.get_a_list() if symbol is None else DataFrame().from_dict(symbol)

    strategies = kwargs['strategies']

    response: dict = {
        'items': []
    }
    for item in strategies:
        # print(f'item = {item}')
        if len(codes) == 0:
            response['items'].append({
                'strategy': item.strategy
            })
            logger.debug(f'PipeStrategyFunction() - code list is empty skip {item.strategy}.')
            continue
        args = item.args
        args['symbol'] = codes.to_dict() # .to_dict(orient='list')

        logger.debug(f'pipe strategy call {item.strategy} function.')
        func = strategy.valid(item.strategy, item.args)
        resp = func.exec(args)
        logger.debug(f'pipe strategy call {item.strategy} end.')
        codes = DataFrame(columns=['code', 'name'])
        for i in range(len(resp['items'])):
            r = resp['items'][i]
            codes.loc[i] = [r['code'], r['name']]
        # print(f'func codes = {codes}')
        response['items'].append({
            'strategy': item.strategy,
            'result': resp
        })

    taskManager.set_result(id=id, result=response, duration=(datetime.now() - begin))    
    logger.debug('PipeStrategyFunction:func() end.')        

