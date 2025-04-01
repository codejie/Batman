import unittest
from datetime import datetime, timedelta
from app.database import data as Data
from app.database import dbEngine

class TestHistoryData(unittest.TestCase):
    def setUp(self):
        dbEngine.start()
        # Setup test data dates
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.last_week = (datetime.now() - timedelta(days=50)).strftime("%Y-%m-%d")
        self.test_code = "000001"  # Example stock code
        
    def tearDown(self):
        dbEngine.shutdown()

    def test_get_history_data(self):
        # Assuming the function fetch_history_data is already implemented
        # and it returns a list of dictionaries with keys 'date' and 'close'
        data = Data.get_history_data(Data.Define.TYPE_STOCK, self.test_code, self.last_week, self.today, 'daily', 'qfq')
        print(data)
        # Check if data is not empty
        self.assertTrue(len(data) > 0)
        
        # # Check if the first entry has the expected keys
        # self.assertIn('date', data[0])
        # self.assertIn('close', data[0])
        
        # # Check if the date is within the last week
        # date = datetime.strptime(data[0]['date'], "%Y%m%d")
        # today = datetime.now()
        # self.assertTrue(date >= today - timedelta(days=7))

    def test_get_latest_history_data(self):
        data = Data.get_latest_history_data(Data.Define.TYPE_STOCK, self.test_code, 'daily', 'qfq')
        print(data)
        self.assertTrue(data is not None)

if __name__ == '__main__':
    unittest.main()
