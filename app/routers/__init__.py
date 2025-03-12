from fastapi import APIRouter, FastAPI
from app.routers import holding

def register_routers(app: FastAPI) -> list[APIRouter]:
  app.include_router(holding.router)