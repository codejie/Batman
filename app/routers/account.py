from fastapi import APIRouter, Body, Depends, Header
from pydantic import BaseModel
from datetime import datetime

from app.routers.definition import RequestModel, ResponseModel, verify_token

router = APIRouter(prefix='/account', tags=['account'])

class LoginRequest(RequestModel):
    account: str
    passwd: str

class LoginResult(BaseModel):
    accessToken: str
    refreshToken: str | None = None
    expired: datetime | None = None
    # uid: int
    avatar: str | None = None
    # role

class LoginResponse(ResponseModel):
    result: LoginResult | None = None

@router.post('/login', response_model=LoginResponse, response_model_exclude_unset=True)
async def login(body: LoginRequest = Body()):
    result = LoginResult(accessToken='token-1')
    resp = LoginResponse(code=0, result=result)
    return resp

"""
Logout
"""
class LogoutRequest(RequestModel):
    pass

class LogoutResponse(ResponseModel):
    pass

@router.post('/logout', response_model=LogoutResponse, response_model_exclude_unset=True, dependencies=[Depends(verify_token)])
async def logout(token: str=Header()):
    print(f'logout() with {token}')
    return LogoutResponse(code=0)
"""
Info
"""
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

@router.post('/info', response_model=InfoResponse, response_model_exclude_unset=True)
async def info(body: InfoRequest = Body()):
    return InfoResponse(result=InfoResult())
