from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Depends, Body, verify_token
from app.strategy import Type
from app.strategy.manager import StrategyManager, strategyInstanceManager

router: APIRouter = APIRouter(prefix='/strategy', tags=['strategy'], dependencies=[Depends(verify_token)])

"""
Common Strategy models
"""
class TriggerModel(BaseModel):
    mode: str = 'daily' # delay
    days: str | None = None
    hour: int | None = None
    minute: int | None = None
    seconds: int | None = None
    period: bool = False

class ArgumentModel(BaseModel):
    name: str
    type: str | None
    unit: str | None
    desc: str | None
    value: list[dict[str, str]] | None = None
    default: str | int | float | list | dict | None = None
    required: bool = True

class ResultFieldModel(BaseModel):
    name: str
    type: str
    desc: str 

class StrategyModel(BaseModel):
    id: str
    type: int
    name: str
    desc: str
    args: list[ArgumentModel] = None
    algorithms: list[str] = None
    result: list[ResultFieldModel] = None

class InstanceModel(BaseModel):
    id: str
    name: str
    strategy: str
    trigger: TriggerModel
    arg_values: dict | None = None
    algo_values: dict[str, dict] | None = None
    results: list | None = None
    latest_updated: str | None = None
    state: int = 0
    is_removed: bool = False
"""
获取策略列表信息
"""
class InfosRequest(RequestModel):
    type: int | None = None
    name: str = None

class InfosResponse(ResponseModel):
    result: list[StrategyModel] = None

@router.post('/infos', response_model=InfosResponse, response_model_exclude_none=True)
async def infos(body: InfosRequest=Body()):
    results = StrategyManager.get_list(None if body.type is None else Type(body.type))
    ret: list[StrategyModel] = []
    for s in results:
        args: list[ArgumentModel] = []
        for a in s.args:
            args.append(ArgumentModel(name=a.name,
                                      type=a.type,
                                      unit=a.unit,
                                      desc=a.desc,
                                      value=a.value,
                                      default=a.default,
                                      required=a.required))
        rs: list[ResultFieldModel] = []    
        for r in s.result:
            rs.append(ResultFieldModel(name=r.name,
                                  type=r.type,
                                  desc=r.desc))

        algos: list[str] = []
        for al in s.algorithms:
            algos.append(al.name)

        ret.append(StrategyModel(id=s.id,
                              type=s.type.value,
                              name=s.name,
                              desc=s.desc,
                              args=args,
                              algorithms=algos,
                              result=rs))

    return InfosResponse(result=ret)

"""
创建策略实例任务
"""
class CreateInstanceRequest(RequestModel):
    name: str
    trigger: TriggerModel
    strategy: str # strategy id
    arg_values: dict | None = None
    algo_values: dict | None = None

class CreateInstanceResponse(ResponseModel):
    result: str # id

@router.post('/create', response_model=CreateInstanceResponse, response_model_exclude_none=True)
async def create(body: CreateInstanceRequest=Body()):
    trigger = dict(body.trigger)
    id = strategyInstanceManager.add(body.name, body.strategy, trigger, body.arg_values, body.algo_values)
    return CreateInstanceResponse(result=id)

"""
获取策略实例列表
"""
class ListInstanceRequest(RequestModel):
    strategy: str | None = None
    type: str | None = None

class ListInstanceResponse(ResponseModel):
    result: list[InstanceModel]

@router.post('/list', response_model=ListInstanceResponse, response_model_exclude_none=True)
async def list(body: ListInstanceRequest=Body()):
    type = None
    if body.type:
        if body.type.upper() == Type.FILTER.name:
            type = Type.FILTER
        elif body.type.upper() == Type.TRADE.name:
            type = Type.TRADE
        else:
            type = None
    ret = []
    instances = strategyInstanceManager.list(body.strategy, type)
    for inst in instances:
        trigger = TriggerModel.model_validate(obj=inst.trigger)
        ret.append(InstanceModel(id=inst.id,
                                 name=inst.name,
                                 strategy=inst.strategy,
                                 trigger=trigger,
                                 arg_values=inst.arg_values,
                                 algo_values=inst.algo_values,
                                 results=inst.results,
                                 latest_updated=inst.latest_updated,
                                 state=inst.state.value,
                                 is_removed=inst.is_removed))
        
    return ListInstanceResponse(result=ret)
"""
获取策略实例详情
"""
class GetInstanceRequest(RequestModel):
    id: str

class GetInstanceResponse(ResponseModel):
    result: InstanceModel

@router.post('/get', response_model=GetInstanceResponse, response_model_exclude_none=True)
async def get(body: GetInstanceRequest=Body()):
    instance = strategyInstanceManager.get(id=body.id)
    trigger = TriggerModel.model_validate(obj=instance.trigger)
    return GetInstanceResponse(result=InstanceModel(
        id=instance.id,
        name=instance.name,
        strategy=instance.strategy,
        trigger=trigger,
        arg_values=instance.arg_values,
        algo_values=instance.algo_values,
        results=instance.results,
        latest_updated=instance.latest_updated,        
        state=instance.state.value,
        is_removed=instance.is_removed    
    ))

"""
删除策略实例
"""
class RemoveInstanceRequest(RequestModel):
    id: str

class RemoveInstanceResponse(ResponseModel):
    result: str

@router.post('/remove', response_model=RemoveInstanceResponse, response_model_exclude_none=True)
async def remove(body: RemoveInstanceRequest=Body()):
    id = strategyInstanceManager.remove(body.id)
    return RemoveInstanceResponse(result=id)

"""
设置策略实例定时
"""
class RescheduleInstanceRequest(RequestModel):
    id: str
    trigger: TriggerModel

class RescheduleInstanceResponse(ResponseModel):
    result: str | None = None

@router.post('/reschedule', response_model=RescheduleInstanceResponse, response_model_exclude_none=True)
async def reschedule(body: RescheduleInstanceRequest=Body()):
    id = strategyInstanceManager.set_trigger(body.id, dict(body.trigger))
    return RescheduleInstanceResponse(result=id)