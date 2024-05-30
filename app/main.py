import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse

from app.logger import logger
from app.exception import AppException, AppRouterException
from app.database import dbEngine
from app.task_manager import taskManager
from app.data import task as dataTask

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info('Service Startup.')
        logger.debug('========engine connect')
        dbEngine.start()

        dataTask.init()
        dataTask.update_task()
        # logger.info('system init data check, maybe take a long long time while fist run , please wait..')
        # init_check()
        # logger.info('system init data check end.')

        logger.debug('========taskManager startup')
        taskManager.start()
        # register_system_check()
    except Exception as e:
        logger.error(f'service start error - {e}')
    yield
    try:
        taskManager.shutdown()
        logger.debug('========taskManager shutdown.')
        dbEngine.shutdown()
        logger.debug('========engine shutdown.')
        logger.info('Service Stop.')
    except Exception as e:
        logger.error(f'service shutdown error - {e}')

app = FastAPI(title='Batman', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, e: AppException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {
                'code': -99,
                'message': e.message
            }
        ))

@app.exception_handler(AppRouterException)
async def app_exception_handler(request: Request, e: AppRouterException):
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
        'Version': '0.2'
    }


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(os.path.dirname(os.path.realpath(__file__)) + '/favicon.ico')

# for router in routers.routers:
#     app.include_router(router)