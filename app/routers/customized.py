from fastapi import APIRouter, Depends
from app.routers.common import RequestModel, ResponseModel, verify_token

router: APIRouter = APIRouter(prefix="/customized", tags=["customized"], dependencies=[Depends(verify_token)])