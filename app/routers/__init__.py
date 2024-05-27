from fastapi import APIRouter
from app.routers import account, data, toolkit, strategy, system,quotes

routers: list[APIRouter] = []
routers.extend(data.routers)
routers.append(account.router)
routers.extend(toolkit.routers)
routers.extend(strategy.routers)
routers.extend(system.routers)
routers.extend(quotes.routers)