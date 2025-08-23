import asyncio
import threading
from typing import Optional

class Task:
  NAME: str = "task"
  def __init__(self, name:str, **kwargs):
    self.name = name if name else self.NAME
    self.kwargs = kwargs
    self._asyncio_task: Optional[asyncio.Task] = None

  def set_asyncio_task(self, task: asyncio.Task):
    """Stores the asyncio.Task wrapper for this task instance."""
    self._asyncio_task = task

  def stop(self):
    """Stops (cancels) the individual task."""
    if self._asyncio_task and not self._asyncio_task.done():
      print(f"Sending stop request to task '{self.name}'.")
      self._asyncio_task.cancel()
    else:
      print(f"Task '{self.name}' is not running or already finished.")

  async def run(self, exit_event: asyncio.Event):
    print(f"Task {self.name} started.")
    try:
      while not exit_event.is_set():
        await asyncio.sleep(1)
        print(f"Task {self.name} is running...")
    except asyncio.CancelledError:
      print(f"Task '{self.name}' was stopped (cancelled)." )
    finally:
      print(f"Task {self.name} exiting.")


class TaskManager:
  TASK_EXIT_DELAY: int = 30  # seconds

  def __init__(self):
    self._thread: threading.Thread | None = None
    self._thread_ready: threading.Event = threading.Event()

    self._loop: asyncio.AbstractEventLoop | None = None
    self._exit_event: asyncio.Event = asyncio.Event()
    self._task_queue: asyncio.Queue[Task] = asyncio.Queue()

    self._task_map: dict[str, Task] = {}

  def _task_done_callback(self, task_name: str, fut: asyncio.Future):
    """Callback function to clean up a task when it's done."""
    try:
      fut.result()
    except asyncio.CancelledError:
      print(f"Task '{task_name}' was cancelled.")
    except Exception as e:
      print(f"Task '{task_name}' failed with an exception: {e}")
    
    if task_name in self._task_map:
      del self._task_map[task_name]
      print(f"Task '{task_name}' finished and was removed from tracking.")

  def _start_loop(self):
    self._loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self._loop)
    self._exit_event.clear()

    async def _loop_run():
      while not self._exit_event.is_set():
        try:
          task_instance = self._task_queue.get_nowait()
          
          # Create the asyncio task and link it to our Task instance
          asyncio_task = asyncio.create_task(task_instance.run(self._exit_event))
          task_instance.set_asyncio_task(asyncio_task)
          
          callback = lambda fut: self._task_done_callback(task_instance.name, fut)
          asyncio_task.add_done_callback(callback)

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
      pending = asyncio.all_tasks(self._loop)
      if pending:
        self._loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
      self._loop.close()

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
      return

    print("TaskManager: Shutting down...")
    self._exit_event.set()
    if self._loop and self._loop.is_running():
      self._loop.call_soon_threadsafe(self._loop.stop)
      
    self._thread.join(timeout=self.TASK_EXIT_DELAY)

    if self._thread.is_alive():
      print("TaskManager: ERROR - Thread did not stop in time.")
    else:
      print("TaskManager: Thread exited successfully.")

    self._loop = None
    self._thread = None
    self._thread_ready.clear()

  def get_exit_event(self) -> asyncio.Event:
    return self._exit_event
  
  def set_exit_event(self):
    self._exit_event.set()

  def add_task(self, task: type, name: Optional[str] = None, **kwargs) -> Task:
    instance = task(name=name, **kwargs)
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