# import asyncio
# from datetime import datetime
# import threading

# from fastapi import WebSocket, WebSocketDisconnect
# from app.database.data.define import TYPE_INDEX, TYPE_STOCK, SpotData
# from app.services import InstanceBase, appServices
# from app.database import data as Data, customized as customizedData

# class SpotDataFetchService(InstanceBase):
#   __PERIOD: int = 10

#   def __init__(self, exit_event: threading.Event, **kwargs):
#     super().__init__(exit_event, **kwargs)

#     self.spot_data: dict[str, list[SpotData]] = {} # hour:minute:second, spot_data

#     self.stocks: list[str] = []
#     self.indices: list[str] = []
#     self.uid: dict[int, list[tuple[int, str]]] = {} # uid: [(type, code)]

#     self.clients: list[tuple[int, WebSocket]] = [] # uid: websocket

#     self.__get_customized_records()

#   def __get_customized_records(self) -> None:
#     results = customizedData.select()
#     for result in results:
#       r = result[0]
#       if r.uid not in self.uid:
#         self.uid[r.uid] = []
#       self.uid[r.uid].append((r.type, r.code))

#       if r.type == TYPE_STOCK:
#         self.stocks.append(r.code)
#       elif r.type == TYPE_INDEX:
#         self.indices.append(r.code)
#       else:
#         raise ValueError(f"Unknown type: {r.type}")
          
#   def add_client(self, uid: int,websocket: WebSocket):
#     self.clients.append((uid, websocket))

#   async def remove_client(self, uid: int, websocket: WebSocket):
#     if websocket in self.clients:
#       await websocket.close()
#       self.clients.remove((uid, websocket))

#   def __get_spot_data(self) -> tuple[int, list[SpotData]]:
#     now = datetime.now()
#     if now.hour == 0 and now.minute == 0:
#       self.spot_data.clear()

#     index = f'{now.hour}:{now.minute}:{now.second}'
#     # midnight = datetime.combine(now.date(), datetime.min.time())
#     # seconds = int((now - midnight).total_seconds())
#     self.spot_data[index] = []
#     data = Data.get_spot_data(type=TYPE_STOCK, codes=self.stocks)
#     if len(data) > 0:
#       self.spot_data[index] += data
#     data = Data.get_spot_data(type=TYPE_INDEX, codes=self.indices)
#     if len(data) > 0:
#       self.spot_data[index] += data
    
#     return (index, self.spot_data[index])
      
#   async def run(self):
#     while not self.exit_event.is_set():
#       data = self.__get_spot_data()
#       print(data)
#       for client in self.clients:
#         uid = client[0]
#         if uid not in self.uid:
#           continue
#         d = [d for d in data[1] if (d.type, d.code) in self.uid[uid]]
#         if len(d) == 0:
#           continue
#         msg = {
#           'seconds': data[0],
#           'data': d
#         }
#         try:
#           await client.send_json(msg)
#         except WebSocketDisconnect:
#           print(f"Client {uid} disconnected")
#           await self.remove_client(uid, client)
#         except Exception as e:
#           print(f"Error sending data to client {uid}: {e}")
#           await self.remove_client(uid, client)

#       asyncio.sleep(self.__PERIOD)    
#       # time.sleep(self.__PERIOD)

# spotDataFetchService = appServices.make_instance(SpotDataFetchService)# .run_instance(SpotDataFetchService)

import asyncio
from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect
from app.database.data.define import TYPE_INDEX, TYPE_STOCK, SpotData
from app.services.service import Service
from app.database import data as Data, customized as customizedData

class SpotDataFetchService(Service):
  __PERIOD: int = 5

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.spot_data: dict[str, list[SpotData]] = {} # hour:minute:second, spot_data

    self.stocks: list[str] = []
    self.indices: list[str] = []
    self.uid: dict[int, list[tuple[int, str]]] = {} # uid: [(type, code)]

    self.clients: list[tuple[int, WebSocket]] = [] # uid: websocket

    self.__get_customized_records()

  def __get_customized_records(self) -> None:
    results = customizedData.select()
    for result in results:
      r = result[0]
      if r.uid not in self.uid:
        self.uid[r.uid] = []
      self.uid[r.uid].append((r.type, r.code))

      if r.type == TYPE_STOCK:
        self.stocks.append(r.code)
      elif r.type == TYPE_INDEX:
        self.indices.append(r.code)
      else:
        raise ValueError(f"Unknown type: {r.type}")
          
  def add_client(self, uid: int,websocket: WebSocket):
    self.clients.append((uid, websocket))

  async def remove_client(self, uid: int, websocket: WebSocket):
    if websocket in self.clients:
      await websocket.close()
      self.clients.remove((uid, websocket))

  def __get_spot_data(self) -> tuple[int, list[SpotData]]:
    now = datetime.now()
    if now.hour == 0 and now.minute == 0:
      self.spot_data.clear()

    index = f'{now.hour}:{now.minute}:{now.second}'
    # midnight = datetime.combine(now.date(), datetime.min.time())
    # seconds = int((now - midnight).total_seconds())
    self.spot_data[index] = []
    data = Data.get_spot_data(type=TYPE_STOCK, codes=self.stocks)
    if len(data) > 0:
      self.spot_data[index] += data
    data = Data.get_spot_data(type=TYPE_INDEX, codes=self.indices)
    if len(data) > 0:
      self.spot_data[index] += data
    
    return (index, self.spot_data[index])
      
  async def run(self, stop_event: asyncio.Event):
    try:
      while not stop_event.is_set():
        data = self.__get_spot_data()
        print(data)
        for client in self.clients:
          uid = client[0]
          if uid not in self.uid:
            continue
          d = [d for d in data[1] if (d.type, d.code) in self.uid[uid]]
          if len(d) == 0:
            continue
          msg = {
            'seconds': data[0],
            'data': d
          }
          try:
            await client.send_json(msg)
          except WebSocketDisconnect:
            print(f"Client {uid} disconnected")
            await self.remove_client(uid, client)
          except Exception as e:
            print(f"Error sending data to client {uid}: {e}")
            await self.remove_client(uid, client)

        await asyncio.sleep(SpotDataFetchService.__PERIOD)
        print('running...')
    except Exception as e:
      print(e)
    print('service exit...')

