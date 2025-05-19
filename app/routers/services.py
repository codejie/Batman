from fastapi import APIRouter, WebSocket

from app.routers.common import verify_token
from app.services import serviceScheduler
from app.services.spot_data_fetch import SpotDataFetchService


router: APIRouter = APIRouter(prefix="/services", tags=["Services"])

"""
spot data websocket
"""
@router.websocket('/ws/spot_data')
async def ws_spot_data(websocket: WebSocket, uid=verify_token()):
  await websocket.accept()
  service: SpotDataFetchService = serviceScheduler.get_service(name=SpotDataFetchService.NAME)
  if service:
    service.add_client(uid, websocket)