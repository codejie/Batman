from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Depends, Body, verify_token
from app.strategy import Type, Argument, Result
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

class ResultModel(BaseModel):
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
    results: list[ResultModel] = None

class InstanceModel(BaseModel):
    id: str
    name: str
    strategy: str
    trigger: TriggerModel
    arg_values: dict | None = None
    algo_values: dict[str, dict] | None = None
    state: int = 0
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
        rs: list[ResultModel] = []    
        for r in s.results:
            rs.append(ResultModel(name=r.name,
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
                              results=rs))

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
获取策略实例
"""
class ListInstanceRequest(RequestModel):
    strategy: str | None = None

class ListInstanceResponse(ResponseModel):
    result: list[InstanceModel]

@router.post('/list', response_model=ListInstanceResponse, response_model_exclude_none=True)
async def list(body: ListInstanceRequest=Body()):
    ret = []
    instances = strategyInstanceManager.list(body.strategy)
    for inst in instances:
        trigger = TriggerModel.model_validate(obj=inst.trigger)
        ret.append(InstanceModel(id=inst.id,
                                 name=inst.name,
                                 strategy=inst.strategy,
                                 trigger=trigger,
                                 arg_values=inst.arg_values,
                                 algo_values=inst.algo_values,
                                 state=inst.state.value))
        
    return ListInstanceResponse(result=ret)

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