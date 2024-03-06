import unittest
import sys
sys.path.append('../')

from app.toolkit import adapter
from app.toolkit import ta
from app.data import index

class TestTA(unittest.TestCase):
    def test_ma(self):
        df = index.get_history('000001', '2023-01-01', '2024-01-01')
        df = adapter.df_akshare2standard(df)
        types = ['SMA','EMA','WMA','DEMA','TEMA','TRIMA','KAMA','MAMA','T3']
        ret = ta.MA(types=types, df=df, columns=['Close', 'Open'], periods=[12, 5, 10])
        print(ret)
        self.assertTrue(True)

    def test_bbands(self):
        df = index.get_history('000001', '2023-01-01', '2024-01-01')
        df = adapter.df_akshare2standard(df)
        # types = ['SMA','EMA','WMA','DEMA','TEMA','TRIMA','KAMA','MAMA','T3']
        ret = ta.BBANDS(df=df, columns=['Close'])
        print(ret)
        self.assertTrue(True)