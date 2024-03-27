"""
Finder Strategy APIs
"""

from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel

from app.routers.dependencies import verify_token
from app.routers.define import RequestModel, ResponseModel

from app.scheduler import scheduler
from app.routers.strategy.finder_func_define import getFinderStrategyFunc, validFinderStrategyFunc
from app.routers.strategy.local_cache import getFinderStrategyInstance, removeFinderStrategyInstance, createFinderStrategyInstance

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
    result = scheduler.addFinderStrategyJob(
        strategy = body.strategy,
        func=strategy['func'],
        title=body.title,
        trigger = body.trigger.model_dump(),
        args=body.args)
    
    args = body.args
    args['id'] = result

    createFinderStrategyInstance(result, body.title, body.trigger.model_dump(), body.strategy, args)

    return ScheduleResponse(code=(-1 if result is None else 0), result=result)

"""
获取指定策略实例的结果
"""
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
class InstanceRequest(RequestModel):
    id: str | None = None
    strategy: str | None = None

class InstanceResult(BaseModel):
    id: str
    name: str
    strategy: str
    args: dict | None = None
    response: dict | None = None

class InstanceResponse(ResponseModel):
    result: list[InstanceResult] | InstanceResult | None = None

@router.post('/instance', response_model=InstanceResponse, response_model_exclude_none=True)
async def instance(body: InstanceRequest=Body()):
    instance = getFinderStrategyInstance(id=body.id, strategy=body.strategy)
    if instance is None:
        return InstanceResponse(result=None)
    
    if type(instance) == list:
        result = []
        for inst in instance:
            result.append(InstanceResult(
                id=inst._id,
                name=inst._name,
                trigger=inst._trigger,
                strategy=inst._strategy,
                args=inst._args,
                response=inst._response
            ))
        return InstanceResponse(result=result)
    else:
        return InstanceResponse(result=InstanceResult(
            id=instance._id,
            name=instance._name,
            trigger=instance._trigger,
            strategy=instance._strategy,
            args=instance._args,
            response=instance._response
        ))
        
"""
删除策略实例
"""
class RemoveRequest(RequestModel):
    id: str

class RemoveResponse(ResponseModel):
    pass

@router.post('/remove', response_model=RemoveResponse, response_model_exclude_none=True)
async def remove(body: RemoveRequest=Body()):
    removeFinderStrategyInstance(body.id)
    return RemoveResponse()

"""
更改策略实例执行时间
"""
class RescheduleRequest(RequestModel):
    id: str
    trigger: TriggerRequest

class RescheduleResponse(ResponseModel):
    pass

@router.post('/reschedule', response_model=RescheduleResponse, response_model_exclude_none=True)
async def reschedule(body: RescheduleRequest=Body()):
    scheduler.rescheduleJob(id=body.id, trigger=body.trigger.model_dump())
    return RescheduleResponse()