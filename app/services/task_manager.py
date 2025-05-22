import asyncio
import threading

class Task:
  NAME: str = "Task"
  def __init__(self, exit_event: asyncio.Event, **kwargs):
    self.exit_event = exit_event
    self.kwargs = kwargs

  async def run(self):
    while not self.exit_event.is_set():
      print('running...')
      await asyncio.sleep(1)
    print('task exited')

class TaskManager:
  TASL_EXIT_DELAY: int = 20
  def __init__(self):
    self.tasks: dict[str, asyncio.Task] = {}
    self.exit_event: asyncio.Event = asyncio.Event()
    self.loop = asyncio.new_event_loop()

  def add_task(self, type: Task, **kwargs) -> Task:
    instance = type(self.exit_event, **kwargs)
    self.tasks[type.NAME] = asyncio.create_task(instance.run())
    self.loop.run_until_complete(self.tasks[type.NAME])
    return instance

  def start(self):
    def run_loop(loop):
      asyncio.set_event_loop(loop)
      loop.run_forever()

    self._thread = threading.Thread(target=run_loop, args=(self.loop,))
    self._thread.start()

  async def __check_tasks_exited(self):
    delay = 0
    while not self.exit_event.is_set():
      if delay > TaskManager.TASL_EXIT_DELAY:
        break
      await asyncio.sleep(1)
      delay += 1

  async def shutdown(self):
    self.loop.call_soon_threadsafe(self.exit_event.set)
    # await self.__check_tasks_exited()
    self.loop.call_soon_threadsafe(self.loop.stop)
    self.loop.close()
    self._thread.join()