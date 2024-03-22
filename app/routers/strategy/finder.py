"""
Finder Strategy APIs
"""

from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel

from app.strategy.finder.fs_1 import FS1Strategy
from app.routers.dependencies import verify_token
from app.routers.define import RequestModel, ResponseModel

from app.scheduler import scheduler
from app.routers.strategy.finder_func import FinderStrategyResponse, RapidRaiseFall00FinderStrategy
from app.routers.strategy.func import finderStrategyFuncList

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
    result: list[InfoResult]

@router.post('/info', response_model=InfoResponse, response_model_exclude_none=True)
async def info(body: InfoRequest=Body()):
    result: list[InfoResult] = []
    if body.name is None:
        for k, v in finderStrategyFuncList.items():
            result.append(InfoResult(name=v['name'], desc=v['desc'], strategy=v['strategy']))
    else:
        v = finderStrategyFuncList[body.name]
        result.append(InfoResult(name=v['name'], desc=v['desc'], strategy=v['strategy']))
    return InfoResponse(result=result)

"""
创建Finder策略任务
"""
class TriggerRequest(BaseModel):
    mode: str = 'daily' # 'interval', 'period'
    hour: int | None = None
    minute: int | None = None
    # second: int | None = None
    interval: int | None = None
    period: bool  = False

class ScheduleRequest(RequestModel):
    title: str
    trigger: TriggerRequest
    strategy: str # strategy name
    args: dict | None = None # strategy arguments

class ScheduleResponse(ResponseModel):
    result: str # job id

@router.post('/schedule', response_model=ScheduleResponse, response_model_exclude_none=True)
async def schedule(body: ScheduleRequest=Body()):
    func = finderStrategyFuncList.get(body.strategy)['func']
    result = scheduler.addJob(
        func=func, 
        title=body.title,
        mode='daily',
        days='0-4',
        hour=body.trigger.hour,
        minute=body.trigger.minute,
        args=body.args)
    return ScheduleResponse(result=result)

"""
获取指定策略实例的结果
"""
class ResultRequest(RequestModel):
    title: str | None = None
    id: str | None = None

class ResultResponse(ResponseModel):
    result: FinderStrategyResponse

@router.post('/result', response_model=ResultResponse, response_model_exclude_none=True)
async def result(body: ResultRequest=Body()):
    print(RapidRaiseFall00FinderStrategy._response)
    return ResultResponse(result=RapidRaiseFall00FinderStrategy._response)

"""
获取策略实例列表
"""