from typing import Optional
from fastapi import APIRouter, Body, Depends, Header
from pydantic import BaseModel
from datetime import datetime

from app.routers.common import RequestModel, ResponseModel, verify_token

router = APIRouter(prefix='/account', tags=['account'])

class LoginRequest(RequestModel):
    account: str
    passwd: str

class LoginResult(BaseModel):
    accessToken: str
    refreshToken: Optional[str] = None
    expired: Optional[datetime] = None
    # uid: int
    avatar: Optional[str] = None
    # role

class LoginResponse(ResponseModel):
    result: Optional[LoginResult] = None

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

@router.post('/logout', response_model=LogoutResponse, response_model_exclude_unset=True) # , dependencies=[Depends(verify_token)])
async def logout(x_token: str=Header()):
    print(f'logout() with {x_token}')
    return LogoutResponse(code=0)
"""
Info
"""
class InfoRequest(RequestModel):
    token: str

class InfoResult(BaseModel):
    roles: list[str] = ['admin', 'signal']
    name: str = 'BATMAN'
    avatar: Optional[str] = 'https://icons.iconarchive.com/icons/diversity-avatars/avatars/256/batman-icon.png'
    introduction: Optional[str] = None
    email: Optional[str] = None

class InfoResponse(ResponseModel):
    result: InfoResult

@router.post('/info', response_model=InfoResponse, response_model_exclude_unset=True)
async def info(body: InfoRequest = Body()):
    return InfoResponse(result=InfoResult())