from datetime import datetime
import unittest

from app.database import common, dbEngine
from app.data.local_db import index
from app.data.task import index as task

class DB(unittest.TestCase):
  def test_index(self):
    dbEngine.start()
    index.fetch_a_list()
    dbEngine.shutdown()
    self.assertTrue(True)

  def test_index_history(self):
    dbEngine.start()
    start = datetime(year=2024, month=1, day=1)
    end = datetime.now()
    index.fetch_history('000001', start, end)
    dbEngine.shutdown()
    self.assertTrue(True)

  def test_index_check(self):
    dbEngine.start()
    task.init_check()
    task.update_daily()
    dbEngine.shutdown()
    self.assertTrue(True)  