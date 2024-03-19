"""
Finder Strategy APIs
"""

from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel

from app.strategy.finder.fs_1 import FS1Strategy
from app.routers.dependencies import verify_token
from app.routers.define import RequestModel, ResponseModel

router = APIRouter(prefix='/strategy/finder', tags=['strategy', 'finder strategy'], dependencies=[Depends(verify_token)])

"""
获取Finder策略列表
"""
class InfoRequest(RequestModel):
    name: str | None = None

class Argument(BaseModel):
    name: str = ''
    type: str = 'str'
    unit: str = ''
    desc: str = ''
    default: str = ''

class StrategyInfoResult(BaseModel):
    name: str
    desc: str
    args: list

class InfoResult(BaseModel):
    name: str
    desc: str
    strategy: StrategyInfoResult

class InfoResponse(ResponseModel):
    result: list[InfoResult] = []

@router.post('/info', response_model=InfoResponse, response_model_exclude_unset=True)
async def info(body: InfoRequest=Body()):
    result: list[InfoResult] = []
    result.append(InfoResult(name='FS1',
                             desc='全部A股，以收盘和开盘为策略数据。',
                             strategy=StrategyInfoResult(name=FS1Strategy._name, desc=FS1Strategy._desc, args=FS1Strategy._args)))
    return InfoResponse(result=result)

"""
创建Finder策略任务
"""
class TriggerRequest(BaseModel):
    mode: str = 'daily' # 'interval', 'period'
    hour: int | None = None
    minute: int | None = None
    second: int | None = None
    interval: int | None = None
    period: bool  = False

class ScheduleRequest(RequestModel):
    title: str
    trigger: dict
    strategy: str # strategy name
    args: dict # strategy arguments

class ScheduleResponse(ResponseModel):
    pass

@router.post('/schedule', response_model=ScheduleResponse, response_model_exclude_unset=True)
async def schedule(body: ScheduleRequest=Body()):
    # scheduler.
    pass