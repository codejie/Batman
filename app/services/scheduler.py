import asyncio
import threading
import time
from app.services.service import Service

class ServiceScheduler:
  DELAY: int = 1
  def __init__(self):
    self.services: dict[str, Service] = {}
    self._thread: threading.Thread = None
    self.tasks_exited: asyncio.Event = asyncio.Event()

  def register_service(self, type: Service, name: str,  **kwargs) -> Service:
    service = type(**kwargs)
    self.services[name] = service
    return service

  def start(self):
    def run_loop(loop):
      asyncio.set_event_loop(loop)
      loop.run_forever()
      # loop.run_until_complete(loop.shutdown_default_executor())

    async def run_tasks(tasks, event: asyncio.Event):
      results = await asyncio.gather(*tasks)
      if all(item is None for item in results):
        event.set()
      else:
        print("Error: ", results)
      # return results

    self.loop = asyncio.new_event_loop()
    self._thread = threading.Thread(target=run_loop, args=(self.loop,))
    self._thread.start()


    self.stop_event = asyncio.Event()
    self.tasks = [service.run(self.stop_event) for service in self.services.values()]
    asyncio.run_coroutine_threadsafe(run_tasks(self.tasks, self.tasks_exited), self.loop)

    # self.stop_event = asyncio.Event()
    # for service in self.services.values():
    #   asyncio.run_coroutine_threadsafe(service.run(self.stop_event), self.loop)

  async def shutdown(self):
    print("Shutting down service scheduler...")
    self.loop.call_soon_threadsafe(self.stop_event.set)
    # self.stop_event.set()
    # await asyncio.wait(self.tasks, return_when=asyncio.ALL_COMPLETED)
    # await self.tasks_exited.wait()
    while not self.tasks_exited.is_set():
      await asyncio.sleep(1)
    self.loop.call_soon_threadsafe(self.loop.stop)
    self.loop.close
    self._thread.join()

