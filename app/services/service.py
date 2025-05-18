import asyncio


class Service:
  def __init__(self, **kwargs):
      self.kwargs = kwargs

  async def run(self, stop_event: asyncio.Event):
    pass
    # while not stop_event.is_set():
    #   print(f"Service is running with delay seconds.")
    #   await asyncio.sleep(1)