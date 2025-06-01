import asyncio
import threading
import time
import unittest
# from app.services import Instance, InstanceBase, Service, appServices
from app.services import serviceScheduler
from app.services.task_manager import TaskBase, TaskManager

def func(exit_event: threading.Event):
  while not exit_event.is_set():
    print('running...')
    time.sleep(1)

# class MyInstance(InstanceBase):
#   def run(self):
#     while not self.exit_event.is_set():
#       print('running...')
#       time.sleep(1)

class TestService(unittest.TestCase):
    # def setUp(self) -> None:
    #     appServices.start()

    # def tearDown(self) -> None:
    #     appServices.shutdown()

    # # def test_shutdown(self):
    # #     self.service.start()
    # #     self.service.shutdown()
    # #     self.assertFalse(self.service.is_running())

    # def test_run(self):
    #     appServices.run(target=func, exit_event=appServices.exit_event)

    #     time.sleep(5)
    #     appServices.shutdown()
    #     self.assertTrue(True)

    # def test_instance(self):
    #   #  inst = MyInstance(app_service.exit_event)
    #    appServices.run_instance(MyInstance)

    #    time.sleep(5) 
    #    appServices.shutdown()
    #    self.assertTrue(True)

    def setUp(self) -> None:
        # appServices.start()
      # serviceScheduler.start()
      pass

    def tearDown(self) -> None:
      # serviceScheduler.shutdown()
    #     appServices.shutdown()
      pass

    # def test_instance(self):
    #    base = appServices.run_instance(Instance, name="base", delay=2)
    #   #  inst = MyInstance(app_service.exit_event)
    #   #  appServices.run_instance(MyInstance)

    #    time.sleep(5) 
    #    appServices.shutdown()
    #    self.assertTrue(True)    
       
    def test_scheduler(self):
      # serviceScheduler.register_service(type=Service, name="test_service")
      serviceScheduler.start()

      time.sleep(10)
      serviceScheduler.shutdown()
      self.assertTrue(True)

    # def test_start_service(self):
    #   start_services()

    #   time.sleep(10)
    #   self.assertTrue(True)

    async def test_task_manager(self):
        task_manager = TaskManager()
        await task_manager.start()
        await asyncio.sleep(5)
        await task_manager.shutdown()
      
        # task_manager.start()
        # # task_manager.add_task(Task)
        # time.sleep(5)
        # task_manager.shutdown()
        # self.assertTrue(True)

    def test_task_base(self):
        task_base = TaskBase(exit_event=threading.Event())
        asyncio.run(task_base.run())

        time.sleep(5)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
