from fastapi import FastAPI, APIRouter

from app.routers import strategy
routers: list[APIRouter] = []

def register_routers(app: FastAPI):
    print('++++++++')
    app.include_router(strategy.router)