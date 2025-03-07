import unittest

from sqlalchemy import select
from app.database import dbEngine, info as Info
# from app.database.holding import UserHoldingTable

from app.database import holding as HoldingTable


class TestUserHoldingTable(unittest.TestCase):
  def setUp(self):
    # Setup code to initialize the database connection and UserHoldingTable instance
    dbEngine.start()

  def test_insert_record(self):
    # Test data
    record = {
      'user_id': 1
    }

    inst = HoldingTable.UserHoldingTable(**record)
    print(inst)
    
    count = dbEngine.instance_insert(inst)
    print(count)
    self.assertTrue(True)

  # def test_select_record(self):
  #   results = HoldingTable.holding_insert(99, 1, 'AAPL')
  #   print(results)
  #   self.assertTrue(True)

  def test_scalar(self):
    
    result = dbEngine.select_scalars(select(HoldingTable.UserHoldingTable.code).where(HoldingTable.UserHoldingTable.id.in_([1,2,3,4])))
    print(result)
    self.assertTrue(True)

  def tearDown(self):
    dbEngine.shutdown()

if __name__ == '__main__':
  unittest.main()