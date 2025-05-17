import asyncio
import threading
from app.services.service import Service

class ServiceScheduler:
  DELAY: int = 1
  def __init__(self):
    self.services: dict[str, Service] = {}
    self._thread: threading.Thread = None

  def register_service(self, type: Service, name: str,  **kwargs) -> Service:
    service = type(**kwargs)
    self.services[name] = service
    return service

  def start(self):
    def run_loop(loop):
      asyncio.set_event_loop(loop)
      loop.run_forever()

    self.loop = asyncio.new_event_loop()
    self._thread = threading.Thread(target=run_loop, args=(self.loop,), daemon=True)
    self._thread.start()

    self.stop_event = asyncio.Event()
    for service in self.services.values():
      asyncio.run_coroutine_threadsafe(service.run(self.stop_event), self.loop)

  def shutdown(self):
    print("Shutting down service scheduler...")
    self.loop.call_soon_threadsafe(self.stop_event.set)
    self.loop.call_soon_threadsafe(self.loop.stop)
    self.loop.close
    self._thread.join()

