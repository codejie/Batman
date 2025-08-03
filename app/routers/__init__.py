from fastapi import APIRouter, FastAPI
from app.routers import data, data_third, holding, account, funds, system, libs, customized, agent
from app.routers import services

def register_routers(app: FastAPI) -> list[APIRouter]:
  app.include_router(libs.router)
  app.include_router(data.router)
  app.include_router(data_third.router)
  app.include_router(funds.router)
  app.include_router(holding.router)
  app.include_router(customized.router)
  app.include_router(services.router)
  app.include_router(system.router)
  app.include_router(account.router)
  app.include_router(agent.router)

