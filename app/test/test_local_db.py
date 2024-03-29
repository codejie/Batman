import unittest

from app.data import stock

class TestLocalDb(unittest.TestCase):
    def test_a_stock(self):
        df = stock.get_a_code()
        print(df)

        self.assertTrue(True)