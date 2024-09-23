from datetime import datetime
import unittest
from unittest import mock
from app.task_scheduler import taskScheduler

def func():
  print(f'{datetime.now()}')

class Test_Scheduler(unittest.TestCase):
  def test_interval(self):
    taskScheduler.start()

    trigger = {
        'mode': 'interval',
        'seconds': 3600
        # 'mode': 'daily',
        # 'hours': 18,
        # 'minutes': 1
    }

    id = taskScheduler.make_id()
    taskScheduler.make_job(id=id, trigger=trigger, func=func, args=None)

    input('press any key..')
    # mock.patch('builtins.input', return_value='dew')
    # mock.patch('builtins.input', return_value='dew')
    # print(dew)
    taskScheduler.shutdown()
    print('end')
    self.assertTrue(True)

  def test_daily(self):
    taskScheduler.start()
    trigger = {
      'mode': 'daily',
      'days': '0-6',
      'hour': 20,
      'minute': 23
    }
    id = taskScheduler.make_id()
    taskScheduler.make_job(id=id, trigger=trigger, func=func, args=None)
    input('press..')
    taskScheduler.shutdown()
    print('end')
    self.assertTrue(True)    

      
    
if __name__ == '__main__':
    unittest.main()   