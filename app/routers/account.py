from fastapi import APIRouter, Body
from pydantic import BaseModel
from datetime import datetime

from .. import logger

router = APIRouter(prefix='/account', tags=['account'])

from . import RequestModel, ResponseModel

class LoginRequest(RequestModel):
    account: str
    passwd: str

class LoginResult(BaseModel):
    accessToken: str
    refreshToken: str | None = None
    expired: datetime | None = None


class LoginResponse(ResponseModel):
    result: LoginResult | None = None

@router.post('/login', response_model=LoginResponse, response_model_exclude_unset=True)
async def login(body: LoginRequest = Body()):
    result = LoginResult(accessToken='token-1')
    resp = LoginResponse(code=0, result=result)
    logger.debug(resp)
    return resp

class InfoRequest(RequestModel):
    token: str

class InfoResult(BaseModel):
    roles: list[str] = ['admin', 'signal']
    name: str = 'BATMAN'
    avatar: str | None = 'https://icons.iconarchive.com/icons/diversity-avatars/avatars/256/batman-icon.png'
    introduction: str | None = None
    email: str | None = None

class InfoResponse(ResponseModel):
    result: InfoResult

@router.post('/info', response_model=InfoResponse, response_model_exclude_none=True)
async def info(body: InfoRequest = Body()):
    return InfoResponse(result=InfoResult())
