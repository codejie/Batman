import unittest

from app.database import common
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
            table = common.TableName.make_stock_history_name(code)
            df = common.select(table, ['日期', '收盘', '开盘']) #, '"日期" > "2024-04-01"')
            # print(df)
            algorithm.set_data({
                'close': df['收盘'],
                'open': df['开盘']
            })
            algorithm.run()
        # print('==================end')
        self.assertTrue(True)