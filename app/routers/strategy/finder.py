"""
Finder Strategy APIs
"""

from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel

from app.routers.dependencies import verify_token
from app.routers.define import RequestModel, ResponseModel

from app.scheduler import scheduler
from app.strategy.finder.func import getFinderStrategyFunc, getFinderStrategyFuncList, validFinderStrategyFunc
from app.strategy.finder.func import func_instance as funcInstance, pipe_func_instance as pipeFuncInstance
from app.strategy.finder.func.pipe_func import PipeStrategyFunction

router = APIRouter(prefix='/strategy/finder', tags=['strategy', 'finder strategy'], dependencies=[Depends(verify_token)])


"""
获取Finder策略列表
"""
class FuncRequest(RequestModel):
    name: str | None = None

class Argument(BaseModel):
    name: str = ''
    type: str = 'str'
    unit: str = ''
    desc: str = ''
    default: str = ''

class StrategyFuncResult(BaseModel):
    name: str
    desc: str
    args: list

class FuncResult(BaseModel):
    name: str
    desc: str
    strategy: StrategyFuncResult

class FuncResponse(ResponseModel):
    result: list[FuncResult]

@router.post('/func', response_model=FuncResponse, response_model_exclude_none=True)
async def func(body: FuncRequest=Body()):
    result: list[FuncResult] = []
    if body.name is None:
        for k, v in getFinderStrategyFuncList().items():
            print(f'v = {v}')
            result.append(FuncResult(name=v._name, desc=v._desc, strategy={
                'name': v._strategy._name,
                'desc': v._strategy._desc,
                'args': v._strategy._args
            }))
    else:
        v = getFinderStrategyFunc(body.name)
        if v is None:
            result.append(FuncResult(name=v._name, desc=v._desc, strategy={
                'name': v._strategy._name,
                'desc': v._strategy._desc,
                'args': v._strategy._args
            }))
    return FuncResponse(result=result)

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
    func = validFinderStrategyFunc(body.strategy, body.args)
    if func is None:
        return ScheduleResponse(code=-1, result=f'strategy func {body.strategy} not found.')
    
    args = body.args

    id = scheduler.addDailyJob(func=func.func, args=body.args, days=body.trigger.days, hour=body.trigger.hour, minute=body.trigger.minute)
    args['id'] = id
    funcInstance.create(id, body.title, body.trigger.model_dump(), body.strategy, args)

    return ScheduleResponse(code=(-1 if id is None else 0), result=id)

"""
获取指定策略实例的结果
"""
class ResultRequest(RequestModel):
    # title: str | None = None
    id: str

class ResultResponse(ResponseModel):
    result: dict | str | None = None

@router.post('/result', response_model=ResultResponse, response_model_exclude_none=True)
async def result(body: ResultRequest=Body()):
    instance = funcInstance.get(body.id)
    if instance is None:
        return ResultResponse(code=-1, result=f'strategy {body.id} not found.')
    return ResultResponse(result=instance.response)


"""
获取策略实例列表
"""
class InstanceRequest(RequestModel):
    id: str | None = None
    strategy: str | None = None

class InstanceResult(BaseModel):
    id: str
    title: str
    trigger: dict | None = None
    strategy: str
    args: dict | None = None
    response: dict | None = None

class InstanceResponse(ResponseModel):
    result: list[InstanceResult] | InstanceResult | None = None

@router.post('/instance', response_model=InstanceResponse, response_model_exclude_none=True)
async def instance(body: InstanceRequest=Body()):
    instance = funcInstance.get(id=body.id, strategy=body.strategy)
    if instance is None:
        return InstanceResponse(result=None)
    if type(instance) == list:
        result = []
        for inst in instance:
            result.append(InstanceResult(
                id=inst.id,
                title=inst.title,
                trigger=inst.trigger,
                strategy=inst.strategy,
                args=inst.args,
                response=inst.response
            ))
        return InstanceResponse(result=result)
    else:
        return InstanceResponse(result=InstanceResult(
            id=instance.id,
            title=instance.title,
            trigger=instance.trigger,
            strategy=instance.strategy,
            args=instance.args,
            response=instance.response
        ))
        
"""
删除策略实例
"""
class RemoveRequest(RequestModel):
    id: str

class RemoveResponse(ResponseModel):
    result: str

@router.post('/remove', response_model=RemoveResponse, response_model_exclude_none=True)
async def remove(body: RemoveRequest=Body()):
    funcInstance.remove(body.id)
    return RemoveResponse(result=body.id)

"""
更改策略实例执行时间
"""
class RescheduleRequest(RequestModel):
    id: str
    trigger: TriggerRequest

class RescheduleResponse(ResponseModel):
    result: str

@router.post('/reschedule', response_model=RescheduleResponse, response_model_exclude_none=True)
async def reschedule(body: RescheduleRequest=Body()):
    ret = scheduler.rescheduleJob(id=body.id, trigger=body.trigger.model_dump())
    if ret:
        funcInstance.set_trigger(id, body.trigger.model_dump())
        return RescheduleResponse(result=body.id)
    else:
        return RescheduleResponse(code=-1, result=body.id)

"""
创建组合策略
"""
class StrategyRequest(BaseModel):
    strategy: str
    args: dict | None = None

class PipeScheduleRequest(RequestModel):
    title: str
    trigger: TriggerRequest
    strategies: list[StrategyRequest]

class PipeScheduleResponse(ResponseModel):
    result: str

@router.post('/pipe/schedule', response_model=PipeScheduleResponse, response_model_exclude_none=True)
async def pipe_schedule(body: PipeScheduleRequest=Body()):
    args = {
        'strategies': body.strategies
    }
    id = scheduler.addDailyJob(func=PipeStrategyFunction, args=args, days=body.trigger.days, hour=body.trigger.hour, minute=body.trigger.minute)
    # id = scheduler.addDelayJob(func=PipeStrategyFunction, args=args, seconds=2)

    args['id'] = id
    pipeFuncInstance.create(id, body.title, body.trigger.model_dump(), body.strategies)

    return PipeScheduleResponse(result=id)

"""
获取组合策略实例的结果
"""
class PipeResultRequest(RequestModel):
    id: str

class PipeResultResponse(ResponseModel):
    result: dict | str | None = None

@router.post('/pipe/result', response_model=PipeResultResponse, response_model_exclude_none=True)
async def pipe_result(body: PipeResultRequest=Body()):
    instance = pipeFuncInstance.get(body.id)
    if instance is None:
        return PipeResultResponse(code=-1, result=f'strategy {body.id} not found.')
    return PipeResultResponse(result=instance.response)


"""
获取组合策略实例列表
"""
class PipeInstanceRequest(RequestModel):
    id: str | None = None

class PipeInstanceResult(BaseModel):
    id: str
    title: str
    trigger: dict | None = None
    strategies: list
    args: dict | None = None
    response: dict | None = None

class PipeInstanceResponse(ResponseModel):
    result: list[PipeInstanceResult] | PipeInstanceResult | None = None

@router.post('/pipe/instance', response_model=PipeInstanceResponse, response_model_exclude_none=True)
async def instance(body: PipeInstanceRequest=Body()):
    instance = pipeFuncInstance.get(id=body.id)
    if instance is None:
        return PipeInstanceResponse(result=None)
    if type(instance) == list:
        result = []
        for inst in instance:
            result.append(PipeInstanceResult(
                id=inst.id,
                title=inst.title,
                trigger=inst.trigger,
                strategies=inst.strategies,
                response=inst.response
            ))
        return PipeInstanceResponse(result=result)
    else:
        return PipeInstanceResponse(result=PipeInstanceResult(
            id=instance.id,
            title=instance.title,
            trigger=instance.trigger,
            strategies=instance.strategies,
            response=instance.response
        ))
        
"""
删除组合策略实例
"""
class PipeRemoveRequest(RequestModel):
    id: str

class PipeRemoveResponse(ResponseModel):
    result: str

@router.post('/pipe/remove', response_model=PipeRemoveResponse, response_model_exclude_none=True)
async def remove(body: RemoveRequest=Body()):
    pipeFuncInstance.remove(body.id)
    return PipeRemoveResponse(result=body.id)

"""
更改组合策略实例执行时间
"""
class PipeRescheduleRequest(RequestModel):
    id: str
    trigger: TriggerRequest

class PipeRescheduleResponse(ResponseModel):
    result: str

@router.post('/pipe/reschedule', response_model=PipeRescheduleResponse, response_model_exclude_none=True)
async def reschedule(body: RescheduleRequest=Body()):
    ret = scheduler.rescheduleJob(id=body.id, trigger=body.trigger.model_dump())
    if ret:
        pipeFuncInstance.set_trigger(id, body.trigger.model_dump())
        return PipeRescheduleResponse(result=body.id)
    else:
        return PipeRescheduleResponse(code=-1, result=body.id)