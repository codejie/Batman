from fastapi import APIRouter, Body
from pydantic import BaseModel
from datetime import datetime

from .. import logger

router = APIRouter(prefix='', tags=['auth'])

from . import RequestModel, ResponseModel

class LoginRequest(RequestModel):
    account: int
    passwd: str

class LoginResult(BaseModel):
    token: str
    expired: datetime | None = None


class LoginResponse(ResponseModel):
    result: LoginResult | None = None

@router.post('/login', response_model=LoginResponse, response_model_exclude_unset=True)
async def login(body: LoginRequest = Body()):
    result = {'token': 'Token-1'}
    result['token'] = 'Token-2'
    resp = LoginResponse(code=1, result={'token': 'Token-3'})
    logger.debug(resp)
    return resp
    # return {
    #     'code': 0,
    #     'result': {
    #         'token': 'token-001'
    #     }
    # }