import unittest
from app.database import dbEngine
from app.database import holding

class Test_Holding(unittest.TestCase):
  def test_holding_insert(self):
    dbEngine.start()

    result = holding.insert(
      uid=99,
      type=1,
      code='000001',
      quantity=100,
      expense=1000.2,
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
      code='000001',
      action=0,
      quantity=200,
      expense=2100
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
      expense=120.2,
      comment='test'
    )
    print(result)
    dbEngine.shutdown()
    self.assertTrue(True)

  def test_get_holding(self):
    dbEngine.start()

    result = holding.get_holding(
      uid=99,
      with_removed=True
    )
    print(result)
    dbEngine.shutdown()
    self.assertTrue(True)

  def test_get_record(self):
    dbEngine.start()

    result = holding.get_record(
      uid=99,
      holding=1,
      action=0,
      with_removed=False
    )
    print(result)
    dbEngine.shutdown()
    self.assertTrue(True)

  def test_calc_holding(self):
    dbEngine.start()

    result = holding.calc_holding(
      uid=99,
      with_removed=True
    )
    print(result)
    dbEngine.shutdown()
    self.assertTrue(True)

  def test_get_holding_record(self):
    dbEngine.start()

    result = holding.get_holding_record(
      uid=99
    )
    print(result)
    dbEngine.shutdown()
    self.assertTrue(True)