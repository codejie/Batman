import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse

from app.database import system
from app.logger import logger
from app.exception import AppException
from app.database import dbEngine
from app.routers import register_routers
from app.task_scheduler import taskScheduler
from app.data import task as dataTask
from app.strategy.manager import strategyInstanceManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info('Service Startup.')
        logger.debug('========engine connect')
        dbEngine.start()

        logger.debug('========taskScheduler startup')
        taskScheduler.start()

        logger.debug('========dataTask init')
        dataTask.init()
        dataTask.update_task()

        logger.debug('========strategyInstanceManager startup')
        strategyInstanceManager.start()

        system.insert_info()
    except Exception as e:
        logger.error(f'service start error - {e}')
    yield
    try:
        strategyInstanceManager.shutdown()
        taskScheduler.shutdown()
        logger.debug('========taskScheduler shutdown.')
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
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                'code': e.code,
                'message': e.message
            }
        ))

@app.exception_handler(Exception)
async def app_exception_handler(request: Request, e: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {
                'code': -99,
                'message': str(e)
            }
        ))

# @app.exception_handler([AppRouterException, AppException, AppException])
# async def app_exception_handler(request: Request, e: AppRouterException):
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content=jsonable_encoder(
#             {
#                 'code': e.code,
#                 'message': e.message
#             }
#         ))


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

register_routers(app)