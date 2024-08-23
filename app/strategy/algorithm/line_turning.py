"""
算法：检测线序列发生拐向
"""

import math
from app.strategy.algorithm import Algorithm, Argument, CallbackType, Data, Result


class LineTurningAlgorithm(Algorithm):
  name: str = '线拐向检测'
  desc: str = '检查单个线序列的上行下行的方向改变点'
  args: list[Argument] = [
    Argument(name='direction',
             type='option',
             value=[
               { 'value': 1, 'desc' : '上行（数值增大）'},
               { 'value': -1, 'desc': '下行（数值减小）'},
               { 'value': 0, 'desc': '上下行'}
             ],
             desc='交叉方向',
             default=0,
             required=False),
    Argument(name='diff',
             type='number',
             desc='转向差值条件(value >= |diff|',
             default=0.0,
             required=False)
  ]
  data: list[Data] = [
    Data('series', 'list of number', '连续序列数据')
  ]
  results: list[Result] = [
    Result('direction', '-1/1', '方向（-1:下行; 1:上行)'),
    Result('pos', 'number', '拐点'),
    Result('count', 'number', '拐点到满足转向差值条件间计数'),
    Result('diff', 'number', '转向差值')
  ]

  def __init__(self) -> None:
    super().__init__()
    self.direction = -2
    # self.count = 0
    # self.diff = 0

    self.curent = 0
    # self.vertex = 0

  def set_args(self, values: dict) -> None:
    super().set_args(values)
    self.direction: int = int(self.arg_values['direction'])
    self.diff: float = abs(float(self.arg_values['diff']))

  def set_data(self, values: dict) -> None:
    super().set_data(values)
    self.series = self.data_values['series']
    self.size = len(self.series)
    self.vertex = 0
    self.pos += 1

  def hitCallback(self, direction: int, pos: int, count: int, diff: float) ->bool :
    if self.callback:
      return self.callback(CallbackType.HIT, {
        'direction': direction,
        'pos': pos,
        'count': count,
        'diff': diff
      })
    return True

  def next(self) -> bool:
    if math.isnan(self.series[self.vertex]):
      self.vertex = self.pos
      return True

    diff = self.series[self.vertex] - self.series[self.pos]
    if abs(diff) >= self.diff:
      if diff > 0:
        self.curent = -1
      elif diff < 0:
        self.curent = 1

      if self.curent != self.direction:
        self.direction = self.curent
        self.hitCallback(self.direction, self.pos, self.pos - self.vertex, diff)
        self.vertex = self.pos

    return super().next()
  