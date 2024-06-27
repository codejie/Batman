from fastapi import FastAPI, APIRouter

from app.routers import strategy
from app.routers import account
from app.routers import algorithm

routers: list[APIRouter] = []

def register_routers(app: FastAPI):
    app.include_router(strategy.router)
    app.include_router(account.router)
    app.include_router(algorithm.router)