

from app.services.scheduler import ServiceScheduler
from app.services.service import Service
from app.services.spot_data_fetch import SpotDataFetchService


# serviceThread = None
# spotDataFetchService = SpotDataFetchService()

# def run_loop(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_forever()

# def start_services():
#   loop = asyncio.new_event_loop()
#   threading.Thread(target=run_loop, args=(loop,)).start()
#   asyncio.run_coroutine_threadsafe(spotDataFetchService.run(), loop)



serviceScheduler = ServiceScheduler()
serviceScheduler.register_service(type=Service, name="test_service")
serviceScheduler.register_service(type=SpotDataFetchService, name="spot_data_fetch_service")


# import asyncio
# import threading

# class InstanceBase(threading.Thread):
#   def __init__(self, exit_event: threading.Event, **kwargs):
#     super().__init__()
#     self.exit_event = exit_event

#   def run(self):
#     pass

# class Service:
#   def __init__(self):
#     self.exit_event = threading.Event()
#     self.threads: list[threading.Thread] = [] # no name now

#   def start(self):
#     for t in self.threads:
#       t.start()

#   def run(self, target: callable, **kwargs):
#     t = threading.Thread(target=target, kwargs=kwargs)
#     self.threads.append(t)
#     t.start()

#   def make_instance(self, base: InstanceBase, **kwargs) -> InstanceBase:
#     instance = base(exit_event=self.exit_event, **kwargs)
#     self.threads.append(instance)
#     return instance
  
#   # def run_instance(self, base: InstanceBase, **kwargs) -> InstanceBase:
#   #   instance = base(exit_event=self.exit_event, **kwargs)
#   #   self.threads.append(instance)
#   #   instance.start()
#   #   return instance

#   def shutdown(self):
#     self.exit_event.set()
#     for t in self.threads:
#       t.join()
#     self.threads.clear()

# appServices: Service = Service()
# # base = appServices.make_instance(InstanceBase)

# class Instance:
#   def __init__(self, name: str, delay: int, **kwargs):
#     self.name = name
#     self.delay = delay
#     self.kwargs = kwargs
#     self._exit: bool = False

#   def stop(self):
#     self._exit = True

#   def start(self):
#     async def wrapper_run():
#       while not self._exit:
#         if not await self._run():
#           break
#         await asyncio.sleep(self.delay)

#     try:
#       asyncio.run(wrapper_run())
#     except Exception as e:
#       print(f"Error starting instance {self.name}: {e}")
  
#   async def _run(self) -> bool:
#     print(f"Running instance - {self.name}")
#     return True

# class AppServices:
#   def __init__(self):
#     self.instances: dict[str, Instance] = {}

#   def make_instance(self, type: Instance,  name: str, delay: int, **kwargs) -> Instance:
#     instance = type(name=name, delay=delay, **kwargs)
#     self.instances[name] = instance
#     return instance
  
#   def get_instance(self, name: str) -> Instance | None:
#     return self.instances.get(name)
  
#   def run_instance(self, type: Instance,  name: str, delay: int, **kwargs) -> Instance:
#     instance = type(name=name, delay=delay, **kwargs)
#     self.instances[name] = instance
#     asyncio.run(instance.start())
#     instance.start()
#     return instance
  
#   def start(self):
#     for instance in self.instances.values():
#       instance.start()

#   def shutdown(self):
#     for instance in self.instances.values():
#       instance.stop()

# appServices = AppServices()
# # base = appServices.make_instance(Instance, name="base", delay=2)