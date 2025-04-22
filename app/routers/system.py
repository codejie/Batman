from fastapi import APIRouter, Depends
from app.routers.common import verify_token

router: APIRouter = APIRouter(prefix="/system", tags=["System"], dependencies=[Depends(verify_token)])

@router.post('/db/backup')
async def db_backup():
  pass