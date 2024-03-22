from fastapi import APIRouter
from app.routers import account, data, test, toolkit, strategy

routers: list[APIRouter] = []
routers.extend(data.routers)
routers.append(test.router)
routers.append(account.router)
routers.extend(toolkit.routers)
routers.extend(strategy.routers)