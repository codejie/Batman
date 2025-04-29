from fastapi import APIRouter, FastAPI
from app.routers import data, holding, account, funds, system, data_third_stock, libs, customized

def register_routers(app: FastAPI) -> list[APIRouter]:
  app.include_router(libs.router)
  app.include_router(data.router)
  app.include_router(data_third_stock.router)
  app.include_router(funds.router)
  app.include_router(holding.router)
  app.include_router(customized.router)
  app.include_router(system.router)
  app.include_router(account.router)