"""
算法：连续数据,后一与前一的比率大于(rate)
"""
from app.strategy.algorithm import Algorithm, Argument, Data, Result, CallbackType

class CheckRateThresholdAlgorithm(Algorithm):
    name: str = '比率阈值检查'
    desc: str = '连续数据,后一与前一的比率大于(rate)'
    args: list[Argument] = [
        Argument('days', 'number', '天', '连续天数(<=15days)', 5),
        Argument('rate', 'number', '%', '变化比率', 10)
    ]
    data: list[Data] = [
        Data('data', 'list or series', '连续序列数据')
    ]
    results: list[Result] = [
        Result('pos', 'number', '命中索引点')
    ]

    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def set_args(self, values: dict) -> None:
        super().set_args(values)
        self.days = self.arg_values['days']
        self.rate = self.arg_values['rate'] / 100

    def set_data(self, values) -> None:
        super().set_data(values)
        self.data = self.data_values['data']
        self.size = len(self.data)

    def next(self) -> bool:
        if (self.pos + 1) < self.size:
            rate = (self.data[self.pos + 1] - self.data[self.pos]) / self.data[self.pos]
            if rate >= self.rate:
                self.count += 1
            else:
                self.count = 0

            if self.count == self.days:
                if self.callback:
                    ret = self.callback(CallbackType.HIT.value, {
                        'pos': self.pos
                    })
                    if not ret:
                        return False
                self.count = 0
            
        return True
