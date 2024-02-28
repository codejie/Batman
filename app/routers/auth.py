from fastapi import APIRouter, Body

from ..models.auth import LoginRequest, LoginResult, LoginResponse

from .. import logger

router = APIRouter(prefix='', tags=['auth'])

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