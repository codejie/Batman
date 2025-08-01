import asyncio
import threading
from typing import Optional

class Task:
  NAME: str = "task"
  def __init__(self, name:str, **kwargs):
    self.name = name if name else self.NAME
    self.kwargs = kwargs

  async def run(self, exit_event: asyncio.Event):
    print(f"Task {self.name} started.")

    while not exit_event.is_set():
      await asyncio.sleep(1)
      print(f"Task {self.name} is running...")

    print(f"Task {self.name} exiting.")

  async def is_triggered(self, event: asyncio.Event, timeout: float) -> bool:
    """
    Check if the event is set within the given timeout.
    Returns True if the event is set, False if it times out.
    """
    try:
      await asyncio.wait_for(event.wait(), timeout)
      return True
    except asyncio.TimeoutError:
      return False

"""
TaskManager is a class that manages asynchronous tasks in a separate thread.
It allows adding tasks, starting and stopping the task loop, and managing task instances.
"""
class TaskManager:
  TASK_EXIT_DELAY: int = 30  # seconds

  def __init__(self):
    self._thread: threading.Thread | None = None
    self._thread_ready: threading.Event = threading.Event()

    self._loop: asyncio.AbstractEventLoop | None = None
    self._exit_event: asyncio.Event = asyncio.Event()
    self._task_queue: asyncio.Queue[Task] = asyncio.Queue()

    self._task_map: dict[str, Task] = {}

  def _start_loop(self):
    self._loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self._loop)
    self._exit_event.clear()

    async def _loop_run():
      while not self._exit_event.is_set():
        try:
          task = self._task_queue.get_nowait()
          asyncio.create_task(task.run(self._exit_event))
        except asyncio.QueueEmpty:
          await asyncio.sleep(0.1)
        except Exception as e:
          print(f"Error in task loop: {e}")
          break

    self._loop.call_soon_threadsafe(asyncio.create_task, _loop_run())
    self._thread_ready.set()

    try:
      self._loop.run_forever()
    except RuntimeError as e:
      if str(e) == "Event loop is closed":
        print("Event loop was closed, exiting task manager.")
      else:
        print(f"Unexpected error in event loop: {e}")
        raise e
    finally:
      # self._exit_event.set()
      pending = asyncio.all_tasks(self._loop)
      if pending:
        self._loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
      self._loop.close()
      # self._loop.stop()

  def start(self):
    if self._thread is not None and self._thread.is_alive():
      print("TaskManager is already running.")
      return

    self._exit_event.clear()
    self._loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self._loop)

    self._thread = threading.Thread(target=self._start_loop, name="TaskManagerThread", daemon=True)
    self._thread.start()
    self._thread_ready.wait()

  def shutdown(self):
    if self._thread is None or not self._thread.is_alive():
      print("TaskManager is not running.")
      return

    self._exit_event.set()
    if self._loop and self._loop.is_running():
      self._loop.call_soon_threadsafe(self._loop.stop)
    self._thread.join(timeout=self.TASK_EXIT_DELAY)  # Wait for the thread to finish
    if self._thread.is_alive():
      print("TaskManager thread did not stop in time.")

    self._loop = None
    self._thread = None
    self._thread_ready.clear()

  def get_exit_event(self) -> asyncio.Event:
    return self._exit_event
  
  def set_exit_event(self):
    self._exit_event.set()

  def add_task(self, task: type, name: Optional[str] = None) -> Task:
    instance = task(name=name)
    self.add_instance(instance=instance)
    return instance
  
  def add_instance(self, instance: Task):
    if self._thread is None or not self._thread.is_alive():
      raise RuntimeError("TaskManager is not running. Start it before adding tasks.")
    self._task_map[instance.name] = instance
    self._task_queue.put_nowait(instance) 

  def get_instance(self, name: str) -> Optional[Task]:
    return self._task_map.get(name) 
  
taskManager: TaskManager = TaskManager()