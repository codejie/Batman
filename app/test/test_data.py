import unittest

from app.database import common, dbEngine
from app.data.local_db import index

class DB(unittest.TestCase):
  def test_index(self):
    dbEngine.start()
    index.fetch_a_list()
    dbEngine.shutdown()
    self.assertTrue(True)