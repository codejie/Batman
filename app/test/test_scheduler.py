import unittest

import sys
import os

sys.path.append('../../')
from app.scheduler import scheduler

def func():
    print('====================')

class TestSchduler(unittest.TestCase):
    async def test_scheduler(self):
        await scheduler.start()
        scheduler.addDelayJob(func=func, seconds=3)
        await scheduler.shutdown()

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()        