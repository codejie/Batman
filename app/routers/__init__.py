from fastapi import APIRouter, FastAPI
from app.routers import data, holding, account, funds

def register_routers(app: FastAPI) -> list[APIRouter]:
  app.include_router(data.router)
  app.include_router(funds.router)
  app.include_router(holding.router)
  app.include_router(account.router)