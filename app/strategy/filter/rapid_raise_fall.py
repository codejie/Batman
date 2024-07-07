"""
RapidRaiseFallStrategy
base m_up_n_down algorithm
计算指定数据在指定的范围内的速涨速跌
symbols:
    - all stock
    - special stock list
codes:
    - list[code]
item:
    - open/close
    - low/high
days:
    number
"""
from datetime import datetime, timedelta
from app.exception import AppException
from app.logger import logger
from app.strategy import Strategy, Type, Argument, ResultField
from app.strategy.algorithm.m_up_n_down import MUpNDownAlgorithem, CallbackType

from app.database import stock


class RapidRaiseFallStrategy(Strategy):
    id: str = 'RapidRaiseFallStrategy'
    type: Type = Type.FILTER
    name: str = '速涨急跌'
    desc: str = '计算指定历史行情数据在最近范围内的速涨速跌'
    algorithms: list = [MUpNDownAlgorithem]
    args: list[Argument] = [
        Argument(name='symbols',
                 type='option',
                 desc='筛选范围',
                 value=[
                     { 'value': 'all', 'desc' : '所有A股股票'},
                     { 'value': 'list', 'desc': '指定股票代码列表'}
                    ],
                 default='all',
                 required=False),
        Argument(name='codes',
                 type='list',
                 desc='指定的股票代码列表',
                 default=None,
                 required=False),
        Argument(name='item',
                 type='option',
                 desc='指定行情数据项',
                 value=[
                     { 'value': 'open/close', 'desc': '开盘与收盘'},
                     { 'value': 'low/high', 'desc': '最低与最高'}
                    ],
                 default='open/close',
                 required=False),
        Argument(name='days',
                 type='number',
                 desc='最近天数',
                 unit='天',                
                 default=18,
                 required=False)
    ]
    """
    result item: {
        code
        pos
        date
    }
    """
    result: list[ResultField] = [
        ResultField(name='code',
               type='string',
               desc='代码'
               ),
         ResultField(name='position',
               type='number',
               desc='位置'
               ),              
        ResultField(name='date',
               type='string',
               desc='日期'
               ),
    ]

    @staticmethod
    def func(**kwargs) ->None:
        logger.debug(f'Strategy \'{RapidRaiseFallStrategy.name}\' start.')

        try:
            manager = kwargs['manager']
            id = kwargs['id']
            arg_values = kwargs['values']
            algo_values = kwargs['algo_values']

            # arg_values
            codes = arg_values['codes'] if 'codes' in arg_values else None
            symbols = arg_values['symbols']
            if symbols == 'all':
                df = stock.get_a_list()
                codes = df['code'].to_list()
            if not codes:
                raise AppException('codes list is empty.')

            days = arg_values['days']
            start = (datetime.today() - timedelta(days)).strftime('%Y-%m-%d')
            end = datetime.today().strftime('%Y-%m-%d')

            # algorithm, only one algorithm in this strategy
            results = []
            for code in codes:
                RapidRaiseFallStrategy.__exec_algorithm(results, code, start, end, arg_values, algo_values)
            
            print(results)
            manager.set_results(id, results)

        except Exception as e:
            logger.error(f'Strategy \'{RapidRaiseFallStrategy.name}\' failed - {e}')

        logger.debug(f'Strategy \'{RapidRaiseFallStrategy.name}\' end.')

    @staticmethod
    def __exec_algorithm(results: list, code: str, start: str, end: str, arg_values: dict, algo_values: dict) -> None:

        def callback(event: str, result: dict) -> bool:
            # logger.debug(f'{code} - {event} - {result}')
            if event == CallbackType.HIT:
                logger.debug(f'{code} - {event} - {result}')
                results.append({
                    'code': code,
                    'position': result.pos,
                    'date': df[columns[0]][result.pos]
                })
            return True

        item = arg_values['item']
        columns = ['日期', '开盘', '收盘'] if item == 'open/close' else ['日期', '最低', '最高']
        df = stock.get_history(code, start, end, columns)

        algorithm = MUpNDownAlgorithem()
        algorithm.set_args(algo_values[algorithm.name])
        algorithm.set_data({
            'open': df[columns[1]],
            'close': df[columns[2]]
        })
        algorithm.set_callback(callback)
        algorithm.run()
