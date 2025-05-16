import asyncio


class Service:
  def __init__(self, name: str, delay: int, **kwargs):
      self.name = name
      self.delay = delay
      self.kwargs = kwargs


class ServiceScheduler:
  DELAY: int = 1
  def __init__(self):
    self.services: dict[str, Service] = {}
    self._exit: bool = False

  def register_service(self, service: Service):
    self.services[service.name] = service

  def unregister_service(self, name: str):
    if name in self.services:
      del self.services[name]

  def start(self):
    async def wrapper_run():
      while not self._exit:
        print("Starting service scheduler...")
        await asyncio.sleep(ServiceScheduler.DELAY)

    async def wrapper_main():
      await asyncio.gather(asyncio.to_thread(wrapper_run), asyncio.sleep(10))
      print("main exit")

    asyncio.run(wrapper_main())
  
  def shutdown(self):
    self._exit = True

serviceScheduler = ServiceScheduler()