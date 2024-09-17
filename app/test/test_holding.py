import unittest
from app.database import dbEngine
from app.database import holding

class Test_Holding(unittest.TestCase):
  def test_holding_insert(self):
    dbEngine.start()

    result = holding.insert(
      uid=99,
      type=1,
      code='000005',
      quantity=100,
      deal=1.1,
      cost=120.2,
      comment='test'
    )
    print(result)
    dbEngine.shutdown()
    self.assertTrue(True)

  def test_holding_update(self):
    dbEngine.start()

    result = holding.update(
      uid=99,
      type=1,
      code='000005',
      action=0,
      quantity=200,
      deal=1.1,
      cost=120.2
    )
    print(result)
    dbEngine.shutdown()
    self.assertTrue(True)

  def test_holding_test(self):
    dbEngine.start()

    result = holding.test(
      uid=99,
      type=1,
      code='000001',
      quantity=100,
      deal=1.1,
      cost=120.2,
      comment='test'
    )
    print(result)
    dbEngine.shutdown()
    self.assertTrue(True)