from fastapi import Header
from pydantic import BaseModel

DEFAULT_UID: int = 99

class RequestModel(BaseModel):
  pass

class ResponseModel(BaseModel):
  code: int = 0
  message: str = None

def verify_token(x_token: str=Header()) -> int:
    return DEFAULT_UID

def verify_system_token(x_token: str=Header()) -> int:
   return DEFAULT_UID

# """
# WebSocket Client Manager
# """

# class WSClientManager:
#     def __init__(self, type: int = 0):
#         self.type = type
#         self.clients: dict[int, WebSocket] = {}

#     async def on_connect(self, websocket: WebSocket, uid: int):
#         await websocket.accept()
#         if uid in self.clients:
#             await self.clients[uid].close()
#         self.clients[uid] = websocket

#     async def on_disconnect(self, websocket: WebSocket, uid: int):
#         await websocket.close()
#         del self.clients[uid]

#     def get_client(self, uid: int) -> WebSocket | None:
#         return self.clients.get(uid)
    
#     def shutdown(self):
#         for uid, websocket in self.clients.items():
#             websocket.close()
#         self.clients.clear()

# """
# Spot Data WebSocket Client Manager
# """
# class SpotDataClientManager(WSClientManager):
#   def __init__(self, service: SpotDataFetchService):
#     super().__init__(type=WS_TYPE_SPOT_DATA)
#     self.service = service

#     self.check_event = self.service.create_data_event(self.type)
#     self._exit = False

#   def shutdown(self):
#     self.check_event.set()
#     self._exit = True
#     super().shutdown()

#   async def start(self):
#     while True:
#       await self.check_event.wait()
#       if self._exit:
#         break
#       for uid, websocket in self.clients.items():
#          data = self.service.get_data(uid)
#          if data is None:
#             try:
#               await websocket.send_text(data)
#             except Exception as e:
#               print(f"Error sending data to client {uid}: {e}")
#               await self.on_disconnect(websocket, uid)
#       self.check_event.clear()
