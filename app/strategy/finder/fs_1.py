"""
选股策略一: 连续N天涨幅U%，再连续M天跌幅D%
"""
from . import FinderResult, FinderStrategy

class FS1Result(FinderResult):
    def represent(self, **kwargs) -> str:
        df = kwargs['df']
        ret = super().represent(**kwargs)

        date = df['日期']
        close = df['收盘']
        open = df['开盘']
        up_count = int(kwargs['up_count'])
        down_count = int(kwargs['down_count'])

        for pos in self.index:
            ret += f'\n{pos}'
            print(df[pos-4: pos])

            # for u in range((up_count + down_count), 0, -1):
            #     print(f'{pos} - {u}')
            #     ret = ret + f'\t{date[pos - u]}: {close[pos - u]}-{open[pos - u]}({(close[pos - u] - open[pos - u])/open[pos - u] * 100}%)\n'
        return ret        


class FS1Strategy(FinderStrategy):
    def __init__(self):
        super().__init__('fs1', '连续N天涨幅U%，再连续M天跌幅D%')
        self._result = FS1Result()

        self.upCount = 0
        self.downCount = 0

    def load(self, **kwargs) -> bool:
        self.close = kwargs['close']
        self.open = kwargs['open']
        self.up_count = kwargs['up_count']
        self.down_count = kwargs['down_count']
        self.up_rate = kwargs['up_rate']
        self.down_rate = kwargs['down_count']

        return super().load(**kwargs)

    def _update(self) -> bool:
        self._size = len(self.close)
        return super()._update()

    def _next(self) -> bool:
        rate = (self.close[self._pos] - self.open[self._pos]) / self.open[self._pos]
        if rate >= self.up_rate:
            self.upCount += 1
            self.downCount = 0
        elif rate <= self.down_count:
            if self.upCount >= self.up_count:
                self.downCount += 1
        else:
            self.upCount = 0
            self.downCount = 0

        if self.upCount >= self.up_count and self.downCount >= self.down_count:
            self._result.index.append(self._pos)
            self.upCount = 0
            self.downCount = 0

        return True