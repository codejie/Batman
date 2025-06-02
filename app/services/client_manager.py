
from fastapi import WebSocket


class WSClientManager:
  def __init__(self):
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
  
  def clients(self):
    return self.clients

  def shutdown(self):
    for uid, websocket in self.clients.items():
      websocket.close()
    self.clients.clear()