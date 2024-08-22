from app.database import common
from app.database.tables import TableName
from app.libs.talib.momentum_indicators import MACD
from app.strategy.algorithm.line_cross import LineCrossAlgorithm



class MACDStrategy:
  def __init__(self):
    self.result = {
      'funds': 10000,
      'buy': 0,
      'sell': 0,
      'hold': 0
    }


  def set_symbol(self, code: str):
    table = TableName.make_stock_history_name(code)
    self.df = common.select(table, None)
    self.days = len(self.df) - 2
    self.macd = MACD(self.df['收盘'])

  def run(self):
    algorithm = LineCrossAlgorithm()
    algorithm.set_data({
      'seriesA': self.macd['dif'],
      'seriesB': self.macd['dea']
    })
    algorithm.set_args({
      'direction': 0,
      'diff': 0,
      'count': 2
    })

    def callback(event, result):
      try:
        if result['direction'] == 1:
          self.buy(100, self.df['收盘'][result['pos']])
          print(f'buy:  {self.df['收盘'][result['pos']]} - {self.df['日期'][result['pos']]}')
        else:
          print(f'sell:  {self.df['收盘'][result['pos']]} - {self.df['日期'][result['pos']]}')
          self.sell(100, self.df['收盘'][result['pos']])
      except Exception as e:
        print(f'==={e.args}')

    algorithm.set_callback(callback=callback)
    algorithm.run()

    self.output()

  def buy(self, quantity: int, price: float):
    total = quantity * price
    if total > self.result['funds']:
      raise Exception(f'not enough funds : {self.result['funds']} - {total}')
    self.result['funds'] -= total
    self.result['buy'] += 1
    self.result['hold'] += quantity

  def sell(self, quantity: int, price: float):
    if quantity > self.result['hold']:
      quantity = self.result['hold']
    self['funds'] += quantity * price
    self.result['sell'] += 1
    self['hold'] -= quantity

  def output(self):
    print(self.result)