import asyncio
from dataclasses import dataclass
from datetime import datetime
import json
from app.logger import logger
from fastapi import WebSocket, WebSocketDisconnect
from app.database.data.define import TYPE_INDEX, TYPE_STOCK, SpotData
from app.services.client_manager import WSClientManager
from app.services.service import Service
from app.database import data as Data, customized as customizedData

class CustomizedSpoData:
  def __init__(self, index: str, stocks: list[SpotData] = [], indices: list[SpotData] = []):
    self.index: str = index
    self.stocks: list[SpotData] = stocks
    self.indices: list[SpotData] = indices


class SpotDataFetchService(Service):
  NAME: str = "spot_data_fetch_service"
  __PERIOD: int = 15

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    # self.spot_data: dict[str, CustomizedSpoData] = {} # hour:minute:second, spot_data
    self.spot_data: list[CustomizedSpoData]

    self.stocks: list[str] = []
    self.indices: list[str] = []
    self.uid: dict[int, list[tuple[int, str]]] = {} # uid: [(type, code)]

    self.clients: list[tuple[int, WebSocket]] = [] # uid: websocket
    self.data_events: list[asyncio.Event] = [] # uid: event

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

  def create_data_event(self, id: int) -> asyncio.Event:
    event = asyncio.Event()
    self.data_events.append(event)
    return event
  
  # def add_client(self, uid: int, websocket: WebSocket):
  #   self.clients.append((uid, websocket))

  # async def remove_client(self, uid: int, websocket: WebSocket):
  #   await websocket.close()
  #   self.clients.remove((uid, websocket))

  def __get_spot_data(self) -> CustomizedSpoData:
    now = datetime.now()
    if now.hour == 0 and now.minute == 0:
      self.spot_data.clear()

    index = f'{now.hour}:{now.minute}:{now.second}'
    # midnight = datetime.combine(now.date(), datetime.min.time())
    # seconds = int((now - midnight).total_seconds())
    self.spot_data.append(CustomizedSpoData(
      index=index,
      stocks = Data.get_spot_data(type=TYPE_STOCK, codes=self.stocks),
      indices =  Data.get_spot_data(type=TYPE_INDEX, codes=self.indices)
    ))
    
    return self.spot_data[-1]

  def get_data(self, uid: int, index: str = None) -> CustomizedSpoData | None:
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

  async def run(self, stop_event: asyncio.Event):
    while not stop_event.is_set():
      try:
        self.__get_spot_data()
        for e in self.data_events:
          if not e.is_set():
            e.set()
      except Exception as e:
        logger.error(f'{self.NAME} exception: {e}')
      await asyncio.sleep(SpotDataFetchService.__PERIOD)
    logger.info(f'{self.NAME} exit...')

  # async def run(self, stop_event: asyncio.Event):
  #   try:
  #     while not stop_event.is_set():
  #       data: tuple[str, CustomizedSpoData] = self.__get_spot_data()
  #       print(data)
  #       for client in self.clients:
  #         uid = client[0]
  #         if uid not in self.uid.keys():
  #           continue
          
  #         stocks = [d[1] for d in self.uid[uid] if d[0] == TYPE_STOCK]
  #         indices = [d[1] for d in self.uid[uid] if d[0] == TYPE_INDEX]

  #         msg = {
  #           'index': data[0],
  #           'stocks': [d.to_dict() for d in data[1].stocks if d.代码 in stocks],
  #           'indices': [d.to_dict() for d in data[1].indices if d.代码 in indices]
  #         }

  #         if len(msg['stocks']) == 0 and len(msg['indices']) == 0:
  #           continue 

  #         try:
  #           await client[1].send_text(json.dumps(msg))
  #         except WebSocketDisconnect:
  #           print(f"Client {uid} disconnected")
  #           await self.remove_client(uid, client[1])
  #         except Exception as e:
  #           print(f"Error sending data to client {uid}: {e}")
  #           await self.remove_client(uid, client[1])

  #       await asyncio.sleep(SpotDataFetchService.__PERIOD)
  #   except Exception as e:
  #     logger.error(f'{self.NAME} exception: {e}')
  #   logger.info(f'{self.NAME} exit...')

class SpotDataClientManager(WSClientManager):
  NAME: str = "spot_data_client_manager"
  def __init__(self, service: SpotDataFetchService):
    super().__init__()
    self.service = service

    self.check_event = self.service.create_data_event(self.type)
    self._exit = False

  def shutdown(self):
    self.check_event.set()
    self._exit = True
    super().shutdown()

  async def start(self):
    while True:
      await self.check_event.wait()
      if self._exit:
        break
      for uid, websocket in self.clients.items():
         data = self.service.get_data(uid)
         if data is None:
            try:
              await websocket.send_text(data)
            except Exception as e:
              print(f"Error sending data to client {uid}: {e}")
              await self.on_disconnect(websocket, uid)
      self.check_event.clear()