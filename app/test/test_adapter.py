import unittest
import pandas as pd

import sys
import os

sys.path.append('../')
from app.toolkit import adapter


# from ..app.toolkit import adapters

class TestAdapters(unittest.TestCase):
    def test_columns_translate(self):
        df = pd.DataFrame({
            '开盘':[], '收盘':[], '最高':[], '最低':[]
        })
        ret = adapter.columns_akshare2standard(df.columns)
        # print(ret)
        self.assertTrue(ret == {'开盘': 'Open', '收盘': 'Close', '最高': 'High', '最低': 'Low'})

    def test_columns_rename(self):
        df = pd.DataFrame({
            '开盘':[1,2], '收盘':[3,4], '最高':[5,6], '最低':[7,8], 'what':[9,10]
        })
        ret = adapter.columns_akshare2standard(df.columns)
        df = df.rename(columns=ret)
        # print(df)
        self.assertTrue((df.columns.values == ['Open', 'Close', 'High', 'Low', 'what']).all())

if __name__ == '__main__':
    # print(os.getcwd())
    unittest.main()