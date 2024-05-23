"""
Finder Strategy APIs
"""
from datetime import datetime
from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel

from app.routers.dependencies import verify_token
from app.routers.define import RequestModel, ResponseModel

from app import utils
# from app.scheduler import scheduler
from app.strategy.finder import strategy

from app.task_manager import taskManager

from app.strategy.finder.strategy.pipe_strategy import PipeStrategyFunction

router = APIRouter(prefix='/strategy/finder', tags=['strategy', 'finder strategy'], dependencies=[Depends(verify_token)])


"""
获取Finder策略列表
"""
class InfosRequest(RequestModel):
    name: str | None = None

class Argument(BaseModel):
    name: str = ''
    type: str = 'str'
    unit: str = ''
    desc: str = ''
    default: str = ''

class AlgorithmResult(BaseModel):
    name: str
    desc: str
    args: list

class InfosResult(BaseModel):
    name: str
    desc: str
    algorithm: AlgorithmResult

class InfosResponse(ResponseModel):
    result: list[InfosResult]

@router.post('/infos', response_model=InfosResponse, response_model_exclude_none=True)
async def infos(body: InfosRequest=Body()):
    result: list[InfosResult] = []
    if body.name is None:
        for k, v in strategy.getList().items():
            result.append(InfosResult(name=v._name, desc=v._desc, algorithm={
                'name': v._algorithm._name,
                'desc': v._algorithm._desc,
                'args': v._algorithm._args
            }))
    else:
        v = strategy.get(body.name)
        if v is None:
            result.append(InfosResult(name=v._name, desc=v._desc, algorithm={
                'name': v._algorithm._name,
                'desc': v._algorithm._desc,
                'args': v._algorithm._args
            }))
    return InfosResponse(result=result)

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
    func = strategy.valid(body.strategy, body.args)
    if func is None:
        return ScheduleResponse(code=-1, result=f'strategy func {body.strategy} not found.')
    
    # args = body.args

    # id = scheduler.addDailyJob(func=func.func, args=body.args, days=body.trigger.days, hour=body.trigger.hour, minute=body.trigger.minute)
    # args['id'] = id
    id =taskManager.create_finder_strategy(title=body.title, func=func.func, trigger=body.trigger.model_dump(), strategy=body.strategy, args=body.args)

    return ScheduleResponse(code=(-1 if id is None else 0), result=id)

"""
获取指定策略实例的结果
"""
class ResultRequest(RequestModel):
    # title: str | None = None
    id: str

class InstanceResultResponse(BaseModel):
    runTimes: int = 0
    lastUpdated: str = None
    duration: str = None
    result: dict | None = None

class ResultResponse(ResponseModel):
    result: InstanceResultResponse | str = None

@router.post('/result', response_model=ResultResponse, response_model_exclude_none=True)
async def result(body: ResultRequest=Body()):
    instance = taskManager.get_finder_strategy(body.id)
    if instance is None:
        return ResultResponse(code=-1, result=f'strategy {body.id} not found.')
    return ResultResponse(result=InstanceResultResponse(
        lastUpdated=utils.datetime2String2(instance.lastUpdated),
        duration=utils.timedelta2String(instance.duration),
        result=instance.result
    ))


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
    runTimes: int = 0
    lastUpdated: str = None
    duration: str = None
    result: dict | None = None

class InstanceResponse(ResponseModel):
    result: list[InstanceResult] | InstanceResult | None = None

@router.post('/instance', response_model=InstanceResponse, response_model_exclude_none=True)
async def instance(body: InstanceRequest=Body()):
    instance = taskManager.get_finder_strategy(id=body.id, attach=None if body.strategy is None else ('strategy', body.strategy))
    if instance is None:
        return InstanceResponse(result=None)
    if type(instance) == list:
        result = []
        for inst in instance:
            result.append(InstanceResult(
                id=inst.id,
                title=inst.attach['title'],
                trigger=inst.trigger,
                strategy=inst.attach['strategy'],
                args=inst.attach['args'],
                runTimes = inst.runTimes,
                lastUpdated=utils.datetime2String2(inst.lastUpdated),
                duration=utils.timedelta2String(inst.duration),
                result=inst.result
            ))
        return InstanceResponse(result=result)
    else:
        return InstanceResponse(result=InstanceResult(
            id=instance.id,
            trigger=instance.trigger,
            title=instance.attach['title'],
            strategy=instance.attach['strategy'],
            args=instance.attach['args'],
            runTimes = instance.runTimes,
            lastUpdated=utils.datetime2String2(instance.lastUpdated),
            duration=utils.timedelta2String(instance.duration),      
            result = instance.result
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
    id = taskManager.remove(body.id)
    return RemoveResponse(result=id)

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
    # ret = scheduler.rescheduleJob(id=body.id, trigger=body.trigger.model_dump())
    # if ret:
    id = taskManager.set_trigger(body.id, body.trigger.model_dump())
    return RescheduleResponse(result=id)
    # else:
    #     return RescheduleResponse(code=-1, result=body.id)

"""
调用策略函数
"""
class RunRequest(RequestModel):
    id: str

class RunResponse(ResponseModel):
    result: str

@router.post('/run', response_model=RunResponse, response_model_exclude_none=True)
async def call_func(body: RunRequest=Body()):
    id = taskManager.run_job(body.id)
    return RunResponse(result=id)

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
    # args = {
    #     'strategies': body.strategies
    # }
    # id = scheduler.addDailyJob(func=PipeStrategyFunction, args=args, days=body.trigger.days, hour=body.trigger.hour, minute=body.trigger.minute)
    # # id = scheduler.addDelayJob(func=PipeStrategyFunction, args=args, seconds=2)

    # args['id'] = id
    id = taskManager.create_pipe_finder_strategy(title=body.title, func=PipeStrategyFunction, trigger=body.trigger.model_dump(), strategies=body.strategies)

    return PipeScheduleResponse(result=id)

"""
获取组合策略实例的结果
"""
class PipeResultRequest(RequestModel):
    id: str

class PipeResultResponse(ResponseModel):
    result: InstanceResultResponse | str = None

@router.post('/pipe/result', response_model=PipeResultResponse, response_model_exclude_none=True)
async def pipe_result(body: PipeResultRequest=Body()):
    instance = taskManager.get_pipe_finder_strategy(body.id)
    if instance is None:
        return PipeResultResponse(code=-1, result=f'strategy {body.id} not found.')
    return PipeResultResponse(result=InstanceResultResponse(
        runTimes=instance.runTimes,
        lastUpdated=utils.datetime2String2(instance.lastUpdated),
        duration=utils.timedelta2String(instance.duration),
        result=instance.result
    ))


"""
获取组合策略实例列表
"""
class PipeInstanceRequest(RequestModel):
    id: str | None = None

class PipeInstanceResult(BaseModel):
    id: str
    title: str
    trigger: dict | None = None
    args: dict | None = None
    runTimes: int = 0
    lastUpdated: str = None
    duration: str = None    
    result: dict | None = None

class PipeInstanceResponse(ResponseModel):
    result: list[PipeInstanceResult] | PipeInstanceResult | None = None

@router.post('/pipe/instance', response_model=PipeInstanceResponse, response_model_exclude_none=True)
async def instance(body: PipeInstanceRequest=Body()):
    instance = taskManager.get_pipe_finder_strategy(body.id)
    if instance is None:
        return PipeInstanceResponse(result=None)
    if type(instance) == list:
        result = []
        for inst in instance:
            result.append(PipeInstanceResult(
                id=inst.id,
                trigger=inst.trigger,
                title=inst.attach['title'],
                args=inst.attach['args'],
                runTimes=inst.runTimes,
                lastUpdated=utils.datetime2String2(inst.lastUpdated),
                duration=utils.timedelta2String(inst.duration),
                result=inst.result
            ))
        return PipeInstanceResponse(result=result)
    else:
        return PipeInstanceResponse(result=PipeInstanceResult(
            id=instance.id,
            trigger=instance.trigger,
            title=instance.attach['title'],
            args=instance.attach['args'],
            runTimes=instance.runTimes,
            lastUpdated=utils.datetime2String2(instance.lastUpdated),
            duration=utils.timedelta2String(instance.duration),          
            response=instance.result
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
    id = taskManager.remove(body.id)
    return PipeRemoveResponse(result=id)

"""
更改组合策略实例执行时间
"""
class PipeRescheduleRequest(RequestModel):
    id: str
    trigger: TriggerRequest

class PipeRescheduleResponse(ResponseModel):
    result: str | None

@router.post('/pipe/reschedule', response_model=PipeRescheduleResponse, response_model_exclude_none=True)
async def reschedule(body: RescheduleRequest=Body()):
    # ret = scheduler.rescheduleJob(id=body.id, trigger=body.trigger.model_dump())
    # if ret:
    id = taskManager.set_trigger(id, body.trigger.model_dump())
    return PipeRescheduleResponse(code=-1 if id is None else 0, result=id)
    # else:
    #     return PipeRescheduleResponse(code=-1, result=body.id)