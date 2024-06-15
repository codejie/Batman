import unittest

from app.database import dbEngine
from app.strategy.manager import strategyInstanceManager

class Test_Strategy(unittest.TestCase):
    def test_instance(self):
        dbEngine.start()
        strategyInstanceManager.start()

        trigger = {
            'mode': 'delay',
            'seconds': 5
        }

        id = strategyInstanceManager.add('test', 'RapidRaiseFallStrategy', trigger, {}, {})

        strategyInstanceManager.shutdown()
        dbEngine.shutdown()
        self.assertTrue(True)