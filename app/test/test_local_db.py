import unittest

from app.data import stock
from app import utils

class TestLocalDb(unittest.TestCase):
    def test_a_stock(self):
        df = stock.get_a_list()
        print(df)

        self.assertTrue(True)

    def test_date_convert(self):
        start = '2020-01-01'
        c = utils.dateConvert1(start)

        print(c)
        self.assertEqual('20200101', c)