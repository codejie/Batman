from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from . import routers, AppException

from .models import ResponseModel

app = FastAPI(title='Batman')

for router in routers.routers:
    app.include_router(router)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, e: AppException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                'code': e.code,
                'message': e.message
            }
        ))

@app.get('/')
async def root():
    return {
        'App': 'Batman',
        'Description': 'I am rich.',
        'Version': '0.0.1'
    }