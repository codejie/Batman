import unittest
import sys
sys.path.append('../../')

from app.data import stock

from app.strategy.finder.fs_1 import FS1Result, FS1Strategy

class TestFinderStrategy(unittest.TestCase):
    def test_fs1(self):
        df = stock.get_history('002236', '20230101', '20240101')
        strategy = FS1Strategy()
        # print(strategy)
        strategy.load(close=df['收盘'], open=df['开盘'], up_count=3, up_rate=0.05, down_count=1, down_rate=-0.02)
        result = strategy.run()
        print(result.represent(datetime=df['日期'], close=df['收盘'], open=df['开盘'], up_count=3, up_rate=0.05, down_count=1, down_rate=-0.02))

        self.assertTrue(True)

    def call_fs1(self, code: str) -> FS1Result | None:
        df = stock.get_history(symbol=code, start_date='20240313', end_date='20240318')
        if df is not None and {'开盘','收盘'}.issubset(df.columns):
            strategy = FS1Strategy()
            strategy.load(close=df['收盘'], open=df['开盘'], up_count=3, up_rate=0.09, down_count=1, down_rate=-0.05)
            return strategy.run()
        else:
            return None

    def test_fs1_with_all(self):
        codedf = stock.get_a_code()
        for i, w in codedf.iterrows():
            print(f'{i}: {w['code']} - {w['name']}')
        # print(codedf)
        return
        for u in codedf['证券代码']:
            # print(f'================={u}')
            result = self.call_fs1(u)
            if result is not None and len(result.index) > 0:
                print(f'=========={u} is ok')
                # print(result.represent(datetime=df['日期'], close=df['收盘'], open=df['开盘'], up_count=3, up_rate=0.05, down_count=1, down_rate=-0.02))

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()