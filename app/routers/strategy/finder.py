"""
Finder Strategy APIs
"""

from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel

from app.routers.dependencies import verify_token
from app.routers.define import RequestModel, ResponseModel

from app.scheduler import scheduler
from app.routers.strategy.finder_func_define import getFinderStrategyFunc, validFinderStrategyFunc # finderStrategyFuncList
from app.routers.strategy.local_cache import getFinderStrategyInstance

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
        for k, v in getFinderStrategyFunc().items():
            result.append(InfoResult(name=v['name'], desc=v['desc'], strategy=v['strategy']))
    else:
        v = getFinderStrategyFunc(body.name)
        result.append(InfoResult(name=v['name'], desc=v['desc'], strategy=v['strategy']))
    return InfoResponse(result=result)

"""
创建Finder策略任务
"""
class TriggerRequest(BaseModel):
    mode: str = 'daily' # 'interval', 'period'
    days: str | None = None
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
    result: str | None # job id

@router.post('/schedule', response_model=ScheduleResponse, response_model_exclude_none=True)
async def schedule(body: ScheduleRequest=Body()):
    strategy = validFinderStrategyFunc(body.strategy, body.args)
    if strategy is None:
        return ScheduleResponse(code=-1, result=f'strategy func {body.strategy} not found.')
    result = scheduler.addJob(
        strategy = body.strategy,
        func=strategy['func'],
        title=body.title,
        trigger = body.trigger.model_dump(),
        args=body.args)
    return ScheduleResponse(code=(-1 if result is None else 0), result=result)

"""
获取指定策略实例的结果
"""
# class FinderStrategyResponse(BaseModel):
#     updated: str = ''

class ResultRequest(RequestModel):
    # title: str | None = None
    id: str

class ResultResponse(ResponseModel):
    result: dict | None = None

@router.post('/result', response_model=ResultResponse, response_model_exclude_none=True)
async def result(body: ResultRequest=Body()):
    instance = getFinderStrategyInstance(body.id)
    if instance is None:
        return ResultResponse(code=-1, result=None)
    print(instance)
    print(instance._response)
    return ResultResponse(result=instance._response)

    # print(RapidRaiseFall00FinderStrategy._response)
    # return ResultResponse(result=RapidRaiseFall00FinderStrategy._response)

"""
获取策略实例列表
"""