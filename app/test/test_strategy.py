import unittest

from app.data import stock

from app.strategy.finder.fs_1 import FS1Result, FS1Strategy

class TestFinderStrategy(unittest.TestCase):
    def test_fs1(self):
        df = stock.get_history('002236', '20230101', '20240101')
        print(df[106:112])
        strategy = FS1Strategy()
        print(strategy)
        strategy.load(close=df['收盘'], open=df['开盘'], up_count=3, up_rate=0.08, down_count=1, down_rate=-0.05)
        result = strategy.run()
        print(result.represent(df=df, up_count=3, down_count=1))

        self.assertTrue(True)