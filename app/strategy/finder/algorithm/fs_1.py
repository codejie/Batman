"""
选股策略一: 连续N天涨幅[(Close-Open) or (High-Low)]U%，再连续M天跌幅D%
选股策略一: 连续(N)的两个数据[(Close-Open) or (High-Low)]的比率大于U，再连续(M)个数据小于D
"""
from app.strategy.finder.algorithm import Algorithm, Result

class FS1Result(Result):
    _name: str = 'FS1Result'
    _desc: str = 'FS1Strategy Result'

    def __init__(self) -> None:
        super().__init__()

    def represent(self, **kwargs) -> str:
        ret = super().represent(**kwargs)

        date = kwargs['datetime']
        close = kwargs['close']
        open = kwargs['open']
        up_count = kwargs['up_count']
        down_count = kwargs['down_count']
        up_rate = kwargs['up_rate']
        down_rate = kwargs['down_rate']

        ret += (f'\n策略：连续{up_count}天涨幅' + '{:.2}%'.format(up_rate * 100) + f'，再连续{down_count}天跌幅' + '{:.2}%'.format(down_rate * 100))
        for pos in self.index:
            # ret += f'\n{pos-4}-{pos}====\n'
            ret += '\n'
            for u in range((up_count + down_count) - 1, -1, -1):
                # print(f'{pos} - {u}')
                # ret += f'{pos-u}\n'
                ret += f'\t{date[pos - u]}: [{close[pos - u]}-{open[pos - u]}]' + ' ({:.2f}%)\n'.format((close[pos - u] - open[pos - u])/open[pos - u] * 100)
        return ret        


class FS1Algorithem(Algorithm):
    _name: str = 'FS1Strategy'
    _desc: str = '连续(N)的两个数据[(Close-Open) or (High-Low)]的比率大于U，再连续(M)个数据小于D'

    _args: list = [
        {
            'name': 'up_count',
            'type': 'number',
            'unit': '天',
            'desc': '连续上涨天数',
            'default': 3
        },
        {
            'name': 'up_rate',
            'type': 'number',
            'unit': '%',
            'desc': '每天上涨幅度',
            'default': 9.0       
        },
        {
            'name': 'down_count',
            'type': 'number',
            'unit': '天',
            'desc': '连续下跌天数',
            'default': 1
        },
        {
            'name': 'down_rate',
            'type': 'number',
            'unit': '%',
            'desc': '每天下跌幅度',
            'default': -5.0
        }
    ]

    def __init__(self):
        super().__init__(self._name, self._desc)
        self.result = FS1Result()

        self.upCount = 0
        self.downCount = 0

    def load(self, **kwargs) -> bool:
        self.close = kwargs['close']
        self.open = kwargs['open']
        self.up_count = kwargs['up_count']
        self.down_count = kwargs['down_count']
        self.up_rate = kwargs['up_rate']
        self.down_rate = kwargs['down_rate']

        return super().load(kwargs=kwargs)

    def update(self) -> bool:
        self.size = len(self.close)
        return super().update()

    def next(self) -> bool:
        rate = (self.close[self.pos] - self.open[self.pos]) / self.open[self.pos]
        if rate >= self.up_rate:
            self.upCount += 1
            self.downCount = 0
        elif rate <= self.down_rate:
            if self.upCount >= self.up_count:
                self.downCount += 1
        else:
            self.upCount = 0
            self.downCount = 0

        if (self.upCount >= self.up_count) and (self.downCount >= self.down_count):
            self.result.index.append(self.pos)
            self.upCount = 0
            self.downCount = 0

        return True