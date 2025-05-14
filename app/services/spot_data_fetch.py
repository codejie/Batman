from datetime import datetime
import threading
import time

from fastapi import WebSocket
from app.database.data.define import TYPE_INDEX, TYPE_STOCK, SpotData
from app.services import InstanceBase
from app.database import data as Data, customized as customizedData

class SpotDataFetchService(InstanceBase):
    __PERIOD: int = 5

    def __init__(self, exit_event: threading.Event, **kwargs):
        super().__init__(exit_event, **kwargs)

        self.spot_data: dict[int, list[SpotData]] = {} # seconds, spot_data

        self.stocks: list[str] = []
        self.indices: list[str] = []
        self.uid: dict[int, list[tuple[int, str]]] = {}

        self.clients: list[tuple[int, WebSocket]] = []

        self.__get_customized_records()

    def __get_customized_records(self) -> None:
        results = customizedData.select()
        for r in results:
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

    def remove_client(self, uid: int, websocket: WebSocket):
        if websocket in self.clients:
            self.clients.remove((uid, websocket))

    def __get_spot_data(self) -> tuple[int, list[SpotData]]:
        now = datetime.now()
        midnight = datetime.combine(now.date(), datetime.min.time())
        seconds = (now - midnight).total_seconds()
        self.spot_data[seconds] = []
        data = Data.get_spot_data(type=TYPE_STOCK, codes=self.stocks)
        if len(data) > 0:
            self.spot_data[seconds] += data
        data = Data.get_spot_data(type=TYPE_INDEX, codes=self.indices)
        if len(data) > 0:
            self.spot_data[seconds] += data
        
        return (seconds, self.spot_data[seconds])
        
    def run(self):
        while not self.exit_event.is_set():
            data = self.__get_spot_data()
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
                client.send_json(msg)
                
            time.sleep(self.__PERIOD)

