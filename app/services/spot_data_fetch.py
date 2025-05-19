import asyncio
from dataclasses import dataclass
from datetime import datetime
import json
from app.logger import logger
from fastapi import WebSocket, WebSocketDisconnect
from app.database.data.define import TYPE_INDEX, TYPE_STOCK, SpotData
from app.services.service import Service
from app.database import data as Data, customized as customizedData

class CustomizedSpoData:
  def __init__(self, stocks: list[SpotData] = [], indices: list[SpotData] = []):
    self.stocks: list[SpotData] = stocks
    self.indices: list[SpotData] = indices


class SpotDataFetchService(Service):
  NAME: str = "spot_data_fetch_service"
  __PERIOD: int = 15

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.spot_data: dict[str, CustomizedSpoData] = {} # hour:minute:second, spot_data

    self.stocks: list[str] = []
    self.indices: list[str] = []
    self.uid: dict[int, list[tuple[int, str]]] = {} # uid: [(type, code)]

    self.clients: list[tuple[int, WebSocket]] = [] # uid: websocket

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
          
  def add_client(self, uid: int, websocket: WebSocket):
    self.clients.append((uid, websocket))

  async def remove_client(self, uid: int, websocket: WebSocket):
    await websocket.close()
    self.clients.remove((uid, websocket))

  def __get_spot_data(self) -> tuple[int, CustomizedSpoData]:
    now = datetime.now()
    if now.hour == 0 and now.minute == 0:
      self.spot_data.clear()

    index = f'{now.hour}:{now.minute}:{now.second}'
    # midnight = datetime.combine(now.date(), datetime.min.time())
    # seconds = int((now - midnight).total_seconds())
    self.spot_data[index] = CustomizedSpoData(
      stocks = Data.get_spot_data(type=TYPE_STOCK, codes=self.stocks),
      indices =  Data.get_spot_data(type=TYPE_INDEX, codes=self.indices)
    )
    
    return (index, self.spot_data[index])
      
  async def run(self, stop_event: asyncio.Event):
    try:
      while not stop_event.is_set():
        data: tuple[str, CustomizedSpoData] = self.__get_spot_data()
        print(data)
        for client in self.clients:
          uid = client[0]
          if uid not in self.uid.keys():
            continue
          
          stocks = [d[1] for d in self.uid[uid] if d[0] == TYPE_STOCK]
          indices = [d[1] for d in self.uid[uid] if d[0] == TYPE_INDEX]

          msg = {
            'index': data[0],
            'stocks': [d.to_dict() for d in data[1].stocks if d.代码 in stocks],
            'indices': [d.to_dict() for d in data[1].indices if d.代码 in indices]
          }

          if len(msg['stocks']) == 0 and len(msg['indices']) == 0:
            continue 

          try:
            await client[1].send_text(json.dumps(msg))
          except WebSocketDisconnect:
            print(f"Client {uid} disconnected")
            await self.remove_client(uid, client[1])
          except Exception as e:
            print(f"Error sending data to client {uid}: {e}")
            await self.remove_client(uid, client[1])

        await asyncio.sleep(SpotDataFetchService.__PERIOD)
    except Exception as e:
      logger.error(f'{self.NAME} exception: {e}')
    logger.info(f'{self.NAME} exit...')

