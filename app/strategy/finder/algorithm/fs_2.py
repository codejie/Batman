"""
选股算法二：连续数据(days),后一与前一的比率大于(rate)
"""
from app.strategy.finder.algorithm import Algorithm, Result

class FS2Result(Result):
    __name: str = 'FS2Result'
    __desc: str = 'FS2Stragety Result'


class FS2Algorithem(Algorithm):
    _name: str = 'FS2Algorithem'
    _desc: str = '连续数据(days),后一与前一的比率大于(rate)'
    _args: list = [
        {
            'name': 'days',
            'type': 'number',
            'unit': '天',
            'desc': '连续天数(<=15days)',
            'default': 5
        },
        {
            'name': 'rate',
            'type': 'number',
            'unit': '%',
            'desc': '涨幅',
            'default': 0.1
        },
    ]

    def __init__(self):
        super().__init__(self._name, self._desc)
        self.result = FS2Result()
        self.count = 0
        self.rate = 0

    def load(self, **kwargs) -> bool:
        self.data = kwargs['data']
        self.days = kwargs['days']
        self.rate = kwargs['rate']
        return super().load(kwargs=kwargs)
    
    def update(self) -> bool:
        self.size = len(self.data)
        return super().update()

    def next(self) -> bool:
        if (self.pos + 1) == self.size:
            return False
         
        rate = (self.data[self.pos + 1] - self.data[self.pos]) / self.data[self.pos]
        # print(f'========{self.pos} - {self.data[self.pos + 1]} - {self.data[self.pos]} - {rate}')
        if rate >= self.rate:
            self.count += 1
        else:
            self.count = 0

        if self.count >= (self.days - 1):
            self.result.index.append(self.pos)
            self.count = 0

        return True