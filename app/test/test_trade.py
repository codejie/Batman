import unittest

from app.database import dbEngine
from app.strategy.trade.macd import MACDStrategy

class Test_Trade(unittest.TestCase):
  def test_macd(self):
    dbEngine.start()

    macd = MACDStrategy()
    macd.set_symbol('002236')
    macd.run()

    dbEngine.shutdown()
    self.assertTrue(True)

    