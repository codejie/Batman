import unittest

from app.database import common

class Test_Database(unittest.TestCase):
    def test_select(self):
        df = common.select(table=common.TableName.Stock_A_List, columns=['code'], where='"code" > "000004"', column_trans=['dd'])
        print(df)

        self.assertTrue(True)