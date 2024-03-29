import unittest

import sys
sys.path.append('../')

from app.toolkit import adapter
from app.data import index
from app.toolkit.talib import overlap_studies as ta

class TestTA(unittest.TestCase):
    def test_ma_turbo(self):
        df = index.get_history('000001', '2023-01-01', '2024-01-01')
        df = adapter.df_akshare2standard(df)
        types = ['SMA','EMA','WMA','DEMA','TEMA','TRIMA','KAMA','MAMA','T3']
        ret = ta.MA_turbo(types=types, df=df, columns=['Close', 'Open'], periods=[12, 5, 10])
        print(ret)
        self.assertTrue(True)

    def test_bbands_turbo(self):
        df = index.get_history('000001', '2023-01-01', '2024-01-01')
        df = adapter.df_akshare2standard(df)
        # types = ['SMA','EMA','WMA','DEMA','TEMA','TRIMA','KAMA','MAMA','T3']
        ret = ta.BBANDS_turbo(df=df, columns=['Close'])
        print(ret)
        self.assertTrue(True)

    def test_ma(self):
        df = index.get_history('000001', '2023-01-01', '2024-01-01')
        df = adapter.df_akshare2standard(df)
        ret = ta.MA(df['Close'], 30)
        print(ret)
        self.assertTrue(True)        