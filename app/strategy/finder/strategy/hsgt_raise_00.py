"""
HSGTRaise00StrategyFunction
全部股票连续持股数量(hsgt)变化
"""

from datetime import datetime, timedelta
from pandas import DataFrame
from app import logger
from app.strategy.finder.algorithm.fs_2 import FS2Algorithem, FS2Result

from app.strategy.finder import instance
from app.data import stock

class HSGTRaise00Strategy:
    _name = '北向持股数量变化'
    _desc = '全部股票连续北向持股数量(hsgt)变化'
    _algorithm = FS2Algorithem 

    @staticmethod
    def func(**kwargs):
        logger.debug('HSGTRaise00StrategyFunction:func() called.')
        begin = datetime.now()

        id = kwargs['id']
        response = HSGTRaise00Strategy.exec(kwargs)
        response['updated'] =  datetime.now()
        response['duration'] = f'{(datetime.now() - begin)}'

        instance.set_response(id=id, response=response)
        logger.debug('HSGTRaise00StrategyFunction:func() end.')

    @staticmethod
    def exec(kwargs: dict) -> dict:        
        symbol = kwargs['symbol'] if 'symbol' in kwargs else None
        days = int(kwargs['days'])
        rate = float(kwargs['rate']) / 100

        start = (datetime.today() - timedelta(15)).strftime('%Y-%m-%d')
        end = datetime.today().strftime('%Y-%m-%d')

        response: dict = {
            'items': []
        }

        codes = stock.get_a_list() if symbol is None else DataFrame.from_dict(kwargs['symbol'])
        for index, row in codes.iterrows():
            df = None
            try:
                df = stock.get_hsgt(row['code'], start, end)
            except:
                logger.warn(f'{row['code']} hsgt data is None.')
                continue

            if df is not None and {'持股数量'}.issubset(df.columns):
                df = df.tail(days).reset_index()
                # print(df)
                strategy = FS2Algorithem()
                strategy.load(data=df['持股数量'], days=days, rate=rate)
                result: FS2Result = strategy.run()
                if result.index and len(result.index) > 0:
                    response['items'].append({
                        'code': row['code'],
                        'name': row['name'],
                        'range': f'{df['持股日期'].iloc[0]}~{df['持股日期'].iloc[-1]}',
                        'index': result.index
                    })

        return response            
