import unittest

from app.database import dbEngine
from app.strategy.manager import strategyInstanceManager

class Test_Strategy(unittest.TestCase):
    def test_instance(self):
        dbEngine.start()
        strategyInstanceManager.start()

        id = strategyInstanceManager.add('test', 'RapidRaiseFallStrategy', {}, {}, {})

        strategyInstanceManager.shutdown()
        dbEngine.shutdown()
        self.assertTrue(id = '111')