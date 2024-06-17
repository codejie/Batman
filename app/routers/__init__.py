from fastapi import FastAPI, APIRouter

from app.routers import strategy
routers: list[APIRouter] = []

def register_routers(app: FastAPI):
    app.include_router(strategy.router)