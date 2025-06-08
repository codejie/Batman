from fastapi import APIRouter, WebSocket
from app.routers.common import verify_token
from app.services.task_spot_data import spotDataClientManagerTask


router: APIRouter = APIRouter(prefix="/services", tags=["Services"])

"""
spot data websocket
"""


@router.websocket('/ws/spot_data')
async def ws_spot_data(websocket: WebSocket, uid=verify_token()):
  await spotDataClientManagerTask.on_connect(websocket, uid)
  # try:
  #   while True:
  #     data = await websocket.receive_text()
  #     await websocket.send_text(f"Received: {data}")
  # except Exception as e:
  #   print(f"WebSocket error: {e}")

  # if not manager:
  #   await websocket.accept()
  #   await websocket.send_text("exception: not found spot data service.")
  #   await websocket.close()
  # else:
  #   await manager.on_connect(websocket, uid)
