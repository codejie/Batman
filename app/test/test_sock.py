import unittest

from app.data import stock

class TestSockData(unittest.TestCase):
    def test_code(self):
        df = stock.get_a_code()
        print(df)

        self.assertTrue(True)

    def test_history(self):
        df = stock.get_history('002236', '2023-03-01', '2024-01-01')
        print(df)
        self.assertTrue(True)