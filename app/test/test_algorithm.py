import unittest

from app.database import common
from app.database.tables import TableName
from app.libs.talib.momentum_indicators import MACD
from app.strategy.algorithm.line_cross import LineCrossAlgorithm
from app.strategy.algorithm.line_cross_track import LineCrossTrackAlgorithm
from app.strategy.algorithm.line_turning import LineTurningAlgorithm
from app.strategy.algorithm.m_up_n_down import MUpNDownAlgorithem


class Test_Algorithm(unittest.TestCase):
    def test_m_up_n_down(self):

        def callback(event: str, result: dict) -> bool:
            print(event)
            print(result)            
            if event == 'hit':
                print(f'date = {df['日期'][result['pos']]}')
                return False
            return True

        algorithm = MUpNDownAlgorithem()
        algorithm.set_args({
            'up_count': 3,
            'up_rate': 8,
            'down_count': 1,
            'down_rate': -5           
        })
        algorithm.set_callback(callback=callback)

        stocks = common.select(common.TableName.Stock_A_List)

        codes = stocks['code']
        # codes = codes.iloc[:5]
        for code in codes:
            print(f'============{code}===========')
            # if code != '873001':
            #     continue
            table = TableName.make_stock_history_name(code)
            df = common.select(table, ['日期', '收盘', '开盘']) #, '"日期" > "2024-04-01"')
            # print(df)
            algorithm.set_data({
                'close': df['收盘'],
                'open': df['开盘']
            })
            algorithm.run()
        # print('==================end')
        self.assertTrue(True)

    def test_line_cross(self):
        def callback(event: str, result: dict) -> bool:
            print(event)
            print(result)
            print(df['日期'][result['pos']])

        table = TableName.make_stock_history_name('002236')
        df = common.select(table=table, columns=['日期', '收盘'])

        calcDf = MACD(df['收盘'])

        algorithm = LineCrossAlgorithm()
        algorithm.set_data({
            'seriesA': calcDf['dif'],
            'seriesB': calcDf['dea']
        })
        algorithm.set_callback(callback=callback)
        algorithm.run()

        self.assertTrue(True)

    def test_line_cross_track(self):
        def callback(event, result) -> bool:
            print(result)
        table = TableName.make_stock_history_name('002236')
        df = common.select(table=table, columns=['日期', '收盘'])
        
        calcDf = MACD(df['收盘'])

        algorithm = LineCrossTrackAlgorithm()
        algorithm.set_args({
            'direction': 0,
            'count': 0,
            'diff': 0.2
        })        
        algorithm.set_data({
            'seriesA': calcDf['dif'],
            'seriesB': calcDf['dea']
        })
        algorithm.set_callback(callback=callback)
        algorithm.run()

        self.assertTrue(True)

    def test_line_turning(self):
        def callback(event, hit) -> bool:
            print(hit)
            return True
        table = TableName.make_stock_history_name('002236')
        df = common.select(table=table, columns=['日期', '收盘'], where='WHERE 日期 > "2024-01-01"')
        calcDf = MACD(df['收盘'])

        algorithm = LineTurningAlgorithm()
        algorithm.set_args({
            'direction': 0,
            'diff': 0.0         
        })
        algorithm.set_data({
            'series': calcDf['dif']
        })
        algorithm.set_callback(callback=callback)
        algorithm.run()

        self.assertTrue(True)


            
        