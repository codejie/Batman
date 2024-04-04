import unittest

from app.data import stock
from app.data.remote_api import stock as remote

class TestSockData(unittest.TestCase):
    def test_code(self):
        df = stock.get_a_list()
        print(df)

        self.assertTrue(True)

    def test_history(self):
        df = stock.get_history('002236', '2023-03-01', '2024-01-01')
        print(df)
        self.assertTrue(True)

    def test_individual_hsgt(self):
        df = remote.get_individual_hsgt('002236')
        print(df.columns)

        self.assertTrue(True)

    def test_margin(self):
        df = stock.get_margin('002236', '2024-03-01', '2024-04-01')
        print(df)

        self.assertTrue(True)

    def test_hsgt(self):
        df = stock.get_hsgt('002236', '2024-03-01', '2024-04-01')
        print(df)
        self.assertTrue(True)