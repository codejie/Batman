from fastapi import WebSocket
from app.logger import logger


class WSClientManager:
  def __init__(self):
    self.clients: dict[int, WebSocket] = {}
    self.exit_flag: bool = False

  async def on_connect(self, websocket: WebSocket, uid: int):
    await websocket.accept()
    if uid in self.clients:
        await self.clients[uid].close()
    self.clients[uid] = websocket
    await self.__connection_loop(websocket, uid)

  async def __connection_loop(self, websocket: WebSocket, uid: int):
    try:
      while not self.exit_flag:
        data = await websocket.receive_text()
        # Process the received data if needed
        # await websocket.send_text(f"Received: {data}")
        logger.info(f"Received data from client {uid}: {data}")
    except Exception as e:
      logger.warning(f"WebSocket error for client {uid}: {e}")
      self.on_disconnect(websocket, uid)

  def on_disconnect(self, websocket: WebSocket, uid: int):
    # await websocket.close()
    del self.clients[uid]

  def get_client(self, uid: int) -> WebSocket | None:
    return self.clients.get(uid)
  
  def clients(self):
    return self.clients

  async def shutdown(self):
    self.exit_flag = True
    for uid, websocket in self.clients.items():
      await websocket.close()
    self.clients.clear()