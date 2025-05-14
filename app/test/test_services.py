import threading
import time
import unittest
from app.services import InstanceBase, Service, app_service

def func(exit_event: threading.Event):
  while not exit_event.is_set():
    print('running...')
    time.sleep(1)

class MyInstance(InstanceBase):
  def run(self):
    while not self.exit_event.is_set():
      print('running...')
      time.sleep(1)

class TestService(unittest.TestCase):
    def setUp(self) -> None:
        app_service.start()

    def tearDown(self) -> None:
        app_service.shutdown()

    # def test_shutdown(self):
    #     self.service.start()
    #     self.service.shutdown()
    #     self.assertFalse(self.service.is_running())

    def test_run(self):
        app_service.run(target=func, exit_event=app_service.exit_event)

        time.sleep(5)
        app_service.shutdown()
        self.assertTrue(True)

    def test_instance(self):
       inst = MyInstance(app_service.exit_event)
       app_service.instance(inst)

       time.sleep(5) 
       app_service.shutdown()
       self.assertTrue(True)
       

if __name__ == '__main__':
    unittest.main()
