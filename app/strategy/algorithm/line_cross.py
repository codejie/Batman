"""
算法：A序列与B序列交叉点
"""

from app.strategy.algorithm import Algorithm, Argument, CallbackType, Data, Result


class LineCrossAlgorithm(Algorithm):
  name: str = '线交叉'
  desc: str = '检查两个序列的交叉点(连续)'
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
             desc='交叉后差值条件，value >= |diff|',
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
    Result('pos', 'number', '交叉前点'),
    # Result('pos2', 'number', '交叉后点'),
    Result('direction', '-1/1', '交叉方向，-1：A向下交叉B；1：A向上交叉B'),
    Result('diff', 'number', '交叉后差值')
  ]

  def __init__(self) -> None:
    super().__init__()
    self.up_count = 0
    self.down_count = 0
    self.up_hitted = False
    self.down_hitted = False

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
    def hitCallback(pos, direction, diff):
      # print('hit')
      print(f'{pos} - {direction} - {diff}')
      if self.callback:
        if (self.direction == 0 or self.direction == direction) and (self.diff <= abs(diff)):
          self.callback(CallbackType.HIT, {
            'pos': pos,
            'direction': direction,
            'diff': diff
          })

    if (self.pos + 1) >= self.size:
      return True

    if self.down_hitted:
      if self.A[self.pos] < self.B[self.pos]:
        self.down_count += 1
        if self.down_count >= self.count:
          hitCallback(self.pos, -1, self.A[self.pos] - self.B[self.pos])
          self.down_count = 0
          self.down_hitted = False
      else:
        self.down_count = 0
        self.down_hitted = False
    elif self.up_hitted:
      if self.A[self.pos] > self.B[self.pos]:
        self.up_count += 1
        if self.up_count >= self.count:
          hitCallback(self.pos, 1, self.A[self.pos] - self.B[self.pos])
          self.up_count = 0
          self.up_hitted = False
    else:
      if (self.A[self.pos] >= self.B[self.pos]) and (self.A[self.pos + 1] < self.B[self.pos + 1]):
        # -1, down
        self.down_count += 1
        self.down_hitted = True
        self.up_count = 0
        self.up_hitted = False
        if self.down_count >= self.count:
          hitCallback(self.pos, -1, self.A[self.pos + 1] - self.B[self.pos + 1])
          self.down_count = 0
          self.up_hitted = False
      elif (self.A[self.pos] <= self.B[self.pos]) and (self.A[self.pos + 1] > self.B[self.pos + 1]):
        # 1, up
        self.down_count = 0
        self.down_hitted = False
        self.up_count += 1
        self.up_hitted = True
        if self.up_count >= self.count:
          hitCallback(self.pos, 1, self.A[self.pos + 1] - self.B[self.pos + 1])
          self.up_count = 0
          self.up_hitted = False

    # if (self.A[self.pos] >= self.B[self.pos]) and (self.A[self.pos + 1] < self.B[self.pos + 1]):
    #   # -1, down
    #   self.down_count += 1
    #   self.up_count = 0
    #   self.up_hitted = False
    #   print(f'down = {self.down_count} - {self.down_hitted} - {self.count}')
    #   if not self.down_hitted and self.down_count >= self.count:
    #     hitCallback(self.pos, -1, self.A[self.pos + 1] - self.B[self.pos + 1])
    #     self.down_hitted = True
    # elif (self.A[self.pos] <= self.B[self.pos]) and (self.A[self.pos + 1] > self.B[self.pos + 1]):
    #   # 1, up
    #   self.down_count = 0
    #   self.up_count += 1
    #   self.down_hitted = False
    #   print(f'up = {self.up_count} - {self.up_hitted} - {self.count}')
    #   if not self.up_hitted and self.up_count >= self.count:
    #     hitCallback(self.pos, 1, self.A[self.pos + 1] - self.B[self.pos + 1])
    #     self.up_hitted = True
    # elif self.A[self.pos] == self.B[self.pos]:
    #   if self.A[self.pos + 1] < self.B[self.pos + 1]:
    #     hitCallback(self.pos, -1, self.A[self.pos + 1] - self.B[self.pos + 1])
    #   elif self.A[self.pos + 1] > self.B[self.pos + 1]:
    #     hitCallback(self.pos, 1, self.A[self.pos + 1] - self.B[self.pos + 1])

    return True