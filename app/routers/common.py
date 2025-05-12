from fastapi import Header, WebSocket
from pydantic import BaseModel

DEFAULT_UID: int = 99
WS_SPOT_DATA: int = 1

class RequestModel(BaseModel):
  pass

class ResponseModel(BaseModel):
  code: int = 0
  message: str = None

def verify_token(x_token: str=Header()) -> int:
    return DEFAULT_UID

def verify_system_token(x_token: str=Header()) -> int:
   return DEFAULT_UID

"""
WebSocket Client Manager
"""

class WSClientManager:
    def __init__(self, type: int):
        self.type = type
        self.clients: dict[int, WebSocket] = {}

    async def on_connect(self, websocket: WebSocket, uid: int):
        await websocket.accept()
        if uid in self.clients:
            await self.clients[uid].close()
        self.clients[uid] = websocket

    async def on_disconnect(self, websocket: WebSocket, uid: int):
        await websocket.close()
        del self.clients[uid]

    def get_client(self, uid: int) -> WebSocket | None:
        return self.clients.get(uid)