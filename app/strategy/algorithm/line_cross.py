"""
算法：A序列与B序列交叉点
"""

from app.strategy.algorithm import Algorithm, Argument, CallbackType, Data, Result


class LineCrossAlgorithm(Algorithm):
  name: '线交叉'
  desc: '检查两个序列的交叉点(连续)'
  args: list[Argument] =[]
  data: list[Data] = [
    Data('seriesA', 'list of number', '第一个连续序列数据'),
    Data('seriesB', 'list of number', '第二个连续序列数据')
  ]
  results: list[Result] = [
    Result('pos', 'number', '交叉前点'),
    # Result('pos2', 'number', '交叉后点'),
    Result('direction', '-1/1', '交叉方向，-1：A向下交叉B；1：A向上交叉B')
  ]

  def __init__(self) -> None:
    super().__init__()

  def set_args(self, values: dict) -> None:
    super().set_args(values)

  def set_data(self, values) -> None:
    super().set_data(values)
    self.A = self.data_values['seriesA']
    self.B = self.data_values['seriesB']
    self.size = len(self.A)

  def next(self) -> bool:
    def hitCallback(pos, direction):
      if self.callback:
        self.callback(CallbackType.HIT, {
          'pos': pos,
          'direction': direction
        })

    if (self.pos + 1) >= self.size:
      return True
    
    if (self.A[self.pos] > self.B[self.pos]) and (self.A[self.pos + 1] < self.B[self.pos + 1]):
        # -1, down
      hitCallback(self.pos, -1)
    elif (self.A[self.pos] < self.B[self.pos]) and (self.A[self.pos + 1] > self.B[self.pos + 1]):
      # 1, up
      hitCallback(self.pos, 1)
    elif self.A[self.pos] == self.B[self.pos]:
      if self.A[self.pos + 1] < self.B[self.pos + 1]:
        hitCallback(self.pos, -1)
      elif self.A[self.pos + 1] > self.B[self.pos + 1]:
        hitCallback(self.pos, 1)

    return True