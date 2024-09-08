import unittest
from app.data.remote_api.stock_third import new_high, uptrend

class TestStockThird(unittest.TestCase):
    def test_new_high(self):
        df = new_high(category=0)
        print(df)
        self.assertTrue(df.shape[0] > 0)

    def test_uptrend(self):
        df = uptrend(days=2)
        print(df)
        self.assertTrue(df.shape[0] > 0)    

if __name__ == '__main__':
    unittest.main()