"""
策略组合函数
"""
from pandas import DataFrame
from datetime import datetime
from app.data import stock
from app import logger

from app.strategy.finder.func import validFinderStrategyFunc
from app.strategy.finder.func import pipe_func_instance as pipeFuncInstance
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
        'responses': []
    }
    for item in strategies:
        # print(f'item = {item}')
        if len(codes) == 0:
            response['responses'].append({
                'strategy': item.strategy
            })
            logger.debug(f'PipeStrategyFunction() - code list is empty skip {item.strategy}.')
            continue
        args = item.args
        args['symbol'] = codes # .to_dict(orient='list')

        logger.debug(f'pipe strategy call {item.strategy} function.')
        func = validFinderStrategyFunc(item.strategy, item.args)
        resp = func.exec(args)
        logger.debug(f'pipe strategy call {item.strategy} end.')
        codes = DataFrame(columns=['code', 'name'])
        for i in range(len(resp['items'])):
            r = resp['items'][i]
            codes.loc[i] = [r['code'], r['name']]
        # print(f'func codes = {codes}')
        response['responses'].append({
            'strategy': item.strategy,
            'response': resp
        })

    response['updated'] =  datetime.now()
    response['duration'] = f'{(datetime.now() - begin)}'            
    pipeFuncInstance.set_response(id=id, response=response)
    logger.debug('PipeStrategyFunction:func() end.')        

