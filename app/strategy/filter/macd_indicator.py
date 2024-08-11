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

from app import logger
from app.strategy import Argument, ResultField, Strategy, Type
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
              default=None,
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
             desc='macd signal period argument',
             unit='天',
             default=9,
             required=False),
    Argument(name='direction',
             type='option',
             value=[
               { 'value': '1', 'desc' : '上行交叉'},
               { 'value': '-1', 'desc': '下行交叉'},
               { 'value': '0', 'desc': '全部交叉'}
             ],
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

    logger.debug(f'Strategy \'{MACDIndicatorStrategy.name}\' end.')

  @staticmethod
  def __exec__algorithm() -> list:
    pass