import os
from contextlib import asynccontextmanager
from starlette.types import ASGIApp, Receive, Scope, Send
from apscheduler.schedulers.background import BackgroundScheduler

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from app import routers, AppException

from app.scheduler import scheduler
from app.dbengine import engine, initDb, shutdownDb
from app import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Service Startup.')
    logger.debug('========engine connect')
    initDb(engine=engine)
    logger.debug('========scheduler startup')
    scheduler.start()
    yield
    scheduler.shutdown()
    logger.debug('========scheduler shutdown.')
    shutdownDb(engine=engine)
    logger.debug('========engine shutdown.')
    logger.info('Service Stop.')

app = FastAPI(title='Batman', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

# app.mount('/static', StaticFiles(directory='.\\static'))

@app.get('/')
async def root():
    return {
        'App': 'Batman',
        'Description': 'I am rich.',
        'Version': '0.0.1'
    }


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(os.path.dirname(os.path.realpath(__file__)) + '/favicon.ico')