import unittest

from app.data import stock

class TestSockData(unittest.TestCase):
    def test_code(self):
        df = stock.get_a_code()
        print(df)

        self.assertTrue(True)