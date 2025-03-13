from fastapi import APIRouter, FastAPI
from app.routers import holding, account

def register_routers(app: FastAPI) -> list[APIRouter]:
  app.include_router(holding.router)
  app.include_router(account.router)