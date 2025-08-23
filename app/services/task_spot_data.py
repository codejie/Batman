import asyncio
from datetime import datetime
from typing import Optional

from fastapi.websockets import WebSocketState
from app.logger import logger
from app.database.data.define import TYPE_INDEX, TYPE_STOCK, SpotData
from app.services.__mock import generate_random_spot_data
from app.services.wsclient_manager import WSClientManager
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

  def __init__(self, name: Optional[str] = None, **kwargs):
    super().__init__(name=name if name else SpotDataFetchTask.NAME, **kwargs)

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
  
  def __mock_spot_data(self) -> CustomizedSpoData:
    now = datetime.now()
    index = f'{now.hour}:{now.minute}:{now.second}'
    # stocks = [SpotData(代码='000001', 名称='平安银行', 最新价=10.0, 涨跌=0.5, 涨跌幅=0.05)]
    data = generate_random_spot_data()
    stocks = [data]
    indices = [] # [SpotData(代码='399001', 名称='深证成指', 最新价=15000.0, 涨跌=100.0, 涨跌幅=0.01)]
    
    data = CustomizedSpoData(index=index, stocks=stocks, indices=indices)
    self.spot_data.append(data)
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
        # data = self.__mock_spot_data()
        # print(f'{self.NAME} fetch data: {data.index}, stocks: {len(data.stocks)}, indices: {len(data.indices)}')  # for test
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


class SpotDataClientManagerTask(Task):
  NAME: str = "spot_data_client_manager"

  def __init__(self): #, task: SpotDataFetchTask):
    super().__init__(name=self.NAME)
    self.task: SpotDataFetchTask = None
    self.data_event: asyncio.Event = None # self.task.apply_data_event()

    self.client_manager: WSClientManager = WSClientManager()

  def set_fetch_task(self, task: SpotDataFetchTask):
    self.task = task
    self.data_event = self.task.apply_data_event()

  async def on_connect(self, websocket, uid: int):
    await self.client_manager.on_connect(websocket, uid)
    logger.info(f"Client {uid} connected.")

  async def run(self, exit_event: asyncio.Event):
    while not exit_event.is_set():
      if self.task and self.data_event:
        triggered = await self.is_triggered(event=self.data_event, timeout=0.1)
        if not triggered:
          continue

        for uid, client in self.client_manager.clients.items():
          if client.client_state != WebSocketState.CONNECTED:
            logger.warning(f"Client {uid} is not connected, skipping...")
            self.client_manager.on_disconnect(client, uid)
            continue

          data = self.task.get_data(uid)
          if data is None:
            continue
          try:
            msg = {
              'index': data.index,
              'stocks': [d.to_dict() for d in data.stocks],
              'indices': [d.to_dict() for d in data.indices]
            }
            await client.send_json(msg)
            # await client.send_text('123')
          except Exception as e:
            logger.error(f"Error sending data to client {uid}: {e}")
            self.client_manager.on_disconnect(client, uid)
            continue
        self.data_event.clear()
      else:
        await asyncio.sleep(0.1)

    await self.client_manager.shutdown()
    logger.info(f"{self.NAME} exiting...")

spotDataClientManagerTask = SpotDataClientManagerTask()
