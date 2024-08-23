"""
算法：A序列与B序列交叉点
"""

from app.strategy.algorithm import Algorithm, Argument, CallbackType, Data, Result


class LineCrossTrackAlgorithm(Algorithm):
  name: str = '线交叉跟踪'
  desc: str = '跟踪两个序列的交叉点变化'
  args: list[Argument] =[
    Argument(name='direction',
             type='option',
             value=[
               { 'value': 1, 'desc' : '上行交叉'},
               { 'value': -1, 'desc': '下行交叉'},
               { 'value': 0, 'desc': '全部交叉'}
             ],
             desc='交叉方向',
             default=0,
             required=False),    
    Argument(name='diff',
             type='number',
             desc='交叉后差值条件(value >= |diff|,（交叉后第一个点不检查）)',
             default=0.0,
             required=False),
    Argument(name='count',
             type='number',
             desc='连续交叉计数',
             default=1,
             required=False)
  ]
  data: list[Data] = [
    Data('seriesA', 'list of number', '第一个连续序列数据'),
    Data('seriesB', 'list of number', '第二个连续序列数据')
  ]
  results: list[Result] = [
    Result('changed', 'number', '交叉方向改变,(0:未改变; 1:改变)'),
    Result('direction', '-1/1', '交叉方向（-1:A向下交叉B; 1:A向上交叉B)'),    
    # Result('cross', 'number', '交叉点'),
    Result('pos', 'number', '当前点'),
    Result('count', 'number', '交叉后持续计数(从1起始)'),
    Result('diff', 'number', '交叉差值')
  ]

  def __init__(self) -> None:
    super().__init__()
    # self.changed = 0
    self.direction = -2
    self.count = 0
    # self.pos = 0
    # self.cross = 0

    self.current = 0

  def set_args(self, values: dict) -> None:
    super().set_args(values)
    self.direction: int = int(self.arg_values['direction'])
    self.diff: float = abs(float(self.arg_values['diff']))
    self.count: int = int(self.arg_values['count'])

  def set_data(self, values) -> None:
    super().set_data(values)
    self.A = self.data_values['seriesA']
    self.B = self.data_values['seriesB']
    self.size = len(self.A)

  def next(self) -> bool:
    def hitCallback(changed, direction, pos, count, diff) -> bool:
      if (self.callback) \
        and (direction == 0 or direction == self.direction) \
        and (count >= self.count) \
        and (abs(diff) >=self.diff):
        return self.callback(CallbackType.HIT, {
          'changed': changed,
          'direction': direction,
          'pos': pos,
          'count': count,
          'diff': diff
        })
      return True
    
    diff = self.A[self.pos] - self.B[self.pos]
    if diff > 0:
      self.current = 1
    elif diff < 0:
      self.current = -1

    if self.current != self.direction:
      self.direction = self.current
      self.changed = 1
      self.count = 1
    else:
      self.changed = 0
      self.count += 1
    
    hitCallback(self.changed, self.direction, self.pos, self.count, diff)

    return True