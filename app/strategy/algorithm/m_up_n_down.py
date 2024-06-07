"""
选股策略一: 连续(N)的两个数据[(Close-Open) or (High-Low)]的比率大于U，再连续(M)个数据小于D
"""

from app.strategy.algorithm import Algorithm, Argument, Data, Result


class MUpNDownAlgorithem(Algorithm):
    name: str = '速涨速跌'
    desc: str = '连续(N)的两个数据的差比率大于U，再连续(M)个数据小于D。'
    args: list[Argument] = [
        Argument('up_count', 'number', '天','连续上涨天数', 3),
        Argument('up_rate', 'number', '%','每天上涨幅度', 9.0),
        Argument('down_count', 'number', '天','连续下跌天数', 1),
        Argument('down_rate', 'number', '%','每天下跌幅度', -5.0)
        # {
        #     'name': 'up_count',
        #     'type': 'number',
        #     'unit': '天',
        #     'desc': '连续上涨天数',
        #     'default': 3
        # },
        # {
        #     'name': 'up_rate',
        #     'type': 'number',
        #     'unit': '%',
        #     'desc': '每天上涨幅度',
        #     'default': 9.0       
        # },
        # {
        #     'name': 'down_count',
        #     'type': 'number',
        #     'unit': '天',
        #     'desc': '连续下跌天数',
        #     'default': 1
        # },
        # {
        #     'name': 'down_rate',
        #     'type': 'number',
        #     'unit': '%',
        #     'desc': '每天下跌幅度',
        #     'default': -5.0
        # }
    ]
    data: list[Data] = [
        Data('close', 'list or series', '收盘数据集'),
        Data('open', 'list or series', '开盘数据集')
        # {
        #     'name': 'close',
        #     'type': 'list or series',
        #     'desc': '收盘数据集'
        # },
        # {
        #     'name': 'open',
        #     'type': 'list or series',
        #     'desc': '开盘数据集'
        # }
    ]
    results: list[Result] = [
        Result('pos', 'number', '命中索引点')
        # {
        #     'name': 'pos',
        #     'type': 'number',
        #     'desc': '命中索引点'
        # }
    ]

    def __init__(self) -> None:
        super().__init__()

        self.upCount = 0
        self.downCount = 0

    def set_args(self, values: dict) -> None:
        super().set_args(values)
        self.up_count = self.arg_values['up_count']
        self.down_count = self.arg_values['down_count']
        self.up_rate = self.arg_values['up_rate'] / 100
        self.down_rate = self.arg_values['down_rate'] / 100
    

    def set_data(self, values: dict) -> None:
        super().set_data(values)
        self.close = self.data_values['close']
        self.open = self.data_values['open']
        self.size = len(self.close)

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
        else:
            self.upCount = 0
            self.downCount = 0

        if (self.upCount >= self.up_count) and (self.downCount >= self.down_count):
            if self.callback:
                ret = self.callback('hit', {
                    'pos': self.pos
                })
                if not ret:
                    return False
            self.upCount = 0
            self.downCount = 0

        return True        

    
            

