from fastapi import APIRouter, Body

from ..models.auth import LoginRequest, LoginResponse

router = APIRouter(prefix='', tags=['auth'])

@router.post('/login', response_model=LoginResponse, response_model_exclude_unset=True)
async def login(body: LoginRequest = Body()):
    return {
        'code': 0,
        'result': {
            'account': body.account
        }
    }