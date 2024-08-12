"""
macd_indicator base line_cross algorithm
计算MACD相交线
symbols:
  - all stock
  - special stock list
codes:
  - dataframe([code, name])
data:
  - close
arguments:
  - fast
  - slow
  - period
  - days
  - direction
"""

from datetime import datetime, timedelta
from pandas import DataFrame
from app.logger import logger
from app.database import common, stock
from app.database.tables import TableName
from app.exception import AppException
from app.libs.talib.momentum_indicators import MACD
from app.strategy import Argument, ResultField, Strategy, Type
from app.strategy.algorithm import AlgorithmCallback, CallbackType
from app.strategy.algorithm.line_cross import LineCrossAlgorithm


class MACDIndicatorStrategy(Strategy):
  id: str = 'MACDIndicatorStrategy'
  type: Type = Type.FILTER
  name: str = 'MACD指标'
  desc: str = '基于MACD相交线的指标数据'
  algorithms: list = [LineCrossAlgorithm]
  args: list[Argument] = [
    Argument(name='symbols',
              type='option',
              desc='筛选范围',
              value=[
                { 'value': 'all', 'desc' : '所有A股股票'},
                { 'value': 'list', 'desc': '指定股票代码列表(code,name)'}
              ],
              default='all',
              required=False),
    Argument(name='codes',
              type='dataframe',
              desc='指定的股票代码列表',
              default=None,
              required=False),
    Argument(name='days',
              type='number',
              desc='最近天数范围',
              unit='天',                
              default=26,
              required=False),
    Argument(name='fast',
             type='number',
             desc='macd fast period argument',
             unit='天',
             default=12,
             required=False),
     Argument(name='slow',
             type='number',
             desc='macd slow period argument',
             unit='天',
             default=26,
             required=False),            
    Argument(name='signal',
             type='number',
             desc='macd signal argument',
             unit='天',
             default=9,
             required=False),
    Argument(name='direction',
             type='option',
             value=[
               { 'value': 1, 'desc' : '上行交叉'},
               { 'value': -1, 'desc': '下行交叉'},
               { 'value': 0, 'desc': '全部交叉'}
             ],
             desc='交叉方向',
             default=0,
             required=False)
  ]
  result_fields: list[ResultField] = [
    ResultField(name='code',
            type='string',
            desc='代码'),
    ResultField(name='name',
            type='string',
            desc='名称'),
    ResultField(name='results',
                type='list',
                desc='[position/交叉前位置,date/交叉前日期,direction/交叉方向]')
    # ResultField(name='position',
    #         type='number',
    #         desc='交叉前位置'), 
    # ResultField(name='date',
    #         type='string',
    #         desc='交叉前日期'),
    # ResultField(name='direction',
    #         type='number',
    #         desc='交叉方向')
  ]

  @staticmethod
  def func(**kwargs) -> None:
    logger.debug(f'Strategy \'{MACDIndicatorStrategy.name}\' start.')
    try:
      manager = kwargs['manager']
      id = kwargs['id']
      arg_values = kwargs['values']
      algo_values = kwargs['algo_values']

      symbols = arg_values['symbols']
      codes: DataFrame = DataFrame(arg_values['codes']) if 'codes' in arg_values else None
      if symbols == 'all':
          df = stock.get_a_list()
          # codes = df['code'].to_list()
          codes = df[['code', 'name']]
      if codes.empty:
          raise AppException('codes list is empty.')
      
      days: int = int(arg_values['days'])
      start = (datetime.today() - timedelta(180)).strftime('%Y-%m-%d')
      # end = datetime.today().strftime('%Y-%m-%d')

      fast: int = int(arg_values['fast'])
      slow: int = int(arg_values['slow'])
      signal: int = int(arg_values['signal'])
      direction: int = int(arg_values['direction'])

      code: str = None
      name: str = None

      results = []
      for _, row in codes.iterrows():
        code = row['code']
        name = row['name']
        
        table = TableName.make_stock_history_name(code)
        df = common.select(table=table, columns=['日期', '收盘'], where=f'where 日期 > "{start}" ORDER BY 日期')
        calc_df = MACD(df['收盘'], fast, slow, signal)
          
        hits = MACDIndicatorStrategy.__exec_algorithm(calc_df, direction, days)
        if len(hits) > 0:
          found = False
          for r in results:
            if r['code'] == code:
              for hit in hits:
                r['results'].append({
                  'position': hit['pos'],
                  'date': df['日期'][hit['pos']],
                  'direction': hit['direction']
                })
                found = True
                break
          if not found:
            r = {
               'code': code,
               'name': name,
               'results': []
            }
            for hit in hits:
              r['results'].append({
                'position': hit['pos'],
                'date': df['日期'][hit['pos']],
                'direction': hit['direction']
              })
            results.append(r)  
      
      print(results)
      manager.set_results(id, results, {
        'days': days,
        'start': start   
      })

      logger.debug(f'Strategy \'{MACDIndicatorStrategy.name}\' end.')
    except Exception as e:
      logger.error(f'Strategy \'{MACDIndicatorStrategy.name}\' failed - {e}')

  # @staticmethod
  # def __calc_macd(code: str, start: str, fast: int, slow: int, signal: int) -> DataFrame:
  #   table = TableName.make_stock_history_name(code)
  #   df = common.select(table=table, columns=['日期', '收盘'], where=f'where 日期 > "{start}" ORDER BY 日期')
  #   return MACD(df['收盘'], fast, slow, signal)

  @staticmethod
  def __exec_algorithm(df: DataFrame, direction: int, days: int) -> list:
    results = []
    def callback(event: CallbackType, result: dict) -> bool:
      if event == CallbackType.HIT:
        if direction == 0 or direction == result['direction']:
          results.append({
            'pos': result['pos'],
            'direction': result['direction']
          })

    algorithm = LineCrossAlgorithm()
    algorithm.set_data({
        'seriesA': df['dif'].iloc[-(days - 1)],
        'seriesB': df['dea'].iloc[-(days - 1)]
    })
    algorithm.set_callback(callback)
    algorithm.run()

    return results