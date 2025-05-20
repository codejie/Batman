from fastapi import APIRouter, WebSocket

from app.routers.common import verify_token
from app.services import wsClientManager
from app.services.spot_data_fetch import SpotDataClientManager


router: APIRouter = APIRouter(prefix="/services", tags=["Services"])

"""
spot data websocket
"""


@router.websocket('/ws/spot_data')
async def ws_spot_data(websocket: WebSocket, uid=verify_token()):
  manager = wsClientManager.get(SpotDataClientManager.NAME)
  if not manager:
    await websocket.accept()
    await websocket.send_text("exception: not found spot data service.")
    await websocket.close()
  else:
    await manager.on_connect(websocket, uid)
