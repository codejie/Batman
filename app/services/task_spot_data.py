import asyncio
from datetime import datetime
from typing import Optional
from app.logger import logger
from app.database.data.define import TYPE_INDEX, TYPE_STOCK, SpotData
from app.services.client_manager import WSClientManager
from app.services.task_manager import Task
from app.database import data as Data, customized as customizedData


class CustomizedSpoData:
  def __init__(self, index: str, stocks: list[SpotData] = [], indices: list[SpotData] = []):
    self.index: str = index
    self.stocks: list[SpotData] = stocks
    self.indices: list[SpotData] = indices

class SpotDataFetchTask(Task):
  NAME: str = "spot_data_fetch_task"
  __PERIOD: int = 15

  def __init__(self, **kwargs):
    super().__init__(name=self.NAME, **kwargs)
    self.name = self.NAME

    self.spot_data: list[CustomizedSpoData] = []
    self.stocks: list[str] = []
    self.indices: list[str] = []
    self.uid: dict[int, list[tuple[int, str]]] = {}  # uid: [(type, code)]
    # self.data_events: list[asyncio.Event] = []  # uid: event
    self.data_events: list[asyncio.Event] =[]

    self.__get_customized_records()

  def __get_customized_records(self) -> None:
    results = customizedData.select()
    for result in results:
      r = result[0]
      if r.uid not in self.uid.keys():
        self.uid[r.uid] = []
      self.uid[r.uid].append((r.type, r.code))

      if r.type == TYPE_STOCK:
        self.stocks.append(r.code)
      elif r.type == TYPE_INDEX:
        self.indices.append(r.code)
      else:
        raise ValueError(f"Unknown type: {r.type}")
      
  def __fetch_spot_data(self) -> CustomizedSpoData:
    now = datetime.now()
    if now.hour == 0 and now.minute == 0:
      self.spot_data.clear()

    index = f'{now.hour}:{now.minute}:{now.second}'
    self.spot_data.append(CustomizedSpoData(
      index=index,
      stocks = Data.get_spot_data(type=TYPE_STOCK, codes=self.stocks),
      indices =  Data.get_spot_data(type=TYPE_INDEX, codes=self.indices)
    ))
    
    return self.spot_data[-1]

  def get_data(self, uid: int, index: Optional[str] = None) -> CustomizedSpoData | None:
    if uid not in self.uid.keys():
      return None
    if len(self.spot_data) == 0:
      return None
    data = self.spot_data[-1 if index is None else index]
    
    stocks = [d[1] for d in self.uid[uid] if d[0] == TYPE_STOCK]
    indices = [d[1] for d in self.uid[uid] if d[0] == TYPE_INDEX]

    return CustomizedSpoData(
      index=data.index,
      stocks=[d for d in data.stocks if d.代码 in stocks],
      indices=[d for d in data.indices if d.代码 in indices]
    )
  
  def apply_data_event(self) -> asyncio.Event:
    event = asyncio.Event()
    event.clear()
    self.data_events.append(event)
    return event

  async def run(self, exit_event: asyncio.Event):
    await asyncio.sleep(SpotDataFetchTask.__PERIOD)
    while not exit_event.is_set():
      try:
        self.__fetch_spot_data()
        for e in self.data_events:
          if not e.is_set():
            e.set()
      except Exception as e:
        logger.error(f'{self.NAME} exception: {e}')
      await asyncio.sleep(SpotDataFetchTask.__PERIOD)

    for e in self.data_events:
      if not e.is_set():
        e.set()
    logger.info(f'{self.NAME} exit...')

spotDataFetchTask = SpotDataFetchTask()

class SpotDataClientManagerTask(Task):
  NAME: str = "spot_data_client_manager"

  def __init__(self, task: SpotDataFetchTask):
    super().__init__(type=self.type)
    self.name = self.NAME
    self.task: SpotDataFetchTask = task
    self.data_event: asyncio.Event = self.task.apply_data_event()

    self.client_manager: WSClientManager = WSClientManager()

  async def run(self):
    while not self.exit_event.is_set():
      await self.data_event.wait()
      data = self.task.get_data
      if data:
        for uid, client in self.client_manager.clients.items():
          if not client.is_connected():
            continue
          try:
            msg = {
              'index': data.index,
              'stocks': [d.to_dict() for d in data.stocks],
              'indices': [d.to_dict() for d in data.indices]
            }
            await client.send_json(msg)
          except Exception as e:
            logger.error(f"Error sending data to client {uid}: {e}")
        continue
      self.data_event.clear()

    self.client_manager.shutdown()
    logger.info(f"{self.NAME} exiting...")

spotDataClientManagerTask = SpotDataClientManagerTask(task=spotDataFetchTask)
