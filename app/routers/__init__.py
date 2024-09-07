from fastapi import FastAPI, APIRouter

from app.routers import libs
from app.routers import strategy
from app.routers import account
from app.routers import algorithm
from app.routers import system
from app.routers import data
from app.routers import customized

routers: list[APIRouter] = []

def register_routers(app: FastAPI):
    app.include_router(libs.talib.router)
    app.include_router(data.index.router)    
    app.include_router(data.stock.router)
    app.include_router(data.stock_third.router)
    app.include_router(strategy.router)
    app.include_router(account.router)
    app.include_router(algorithm.router)
    app.include_router(customized.router)
    app.include_router(system.router)