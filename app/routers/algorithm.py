from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Depends, Body, verify_token
from app.strategy.algorithm.manager import AlgorithmManager

router: APIRouter = APIRouter(prefix='/algorithm', tags=['algorithm'], dependencies=[Depends(verify_token)])

"""
Algorithm
"""
class ArgumentModel(BaseModel):
    name: str
    type: str | None
    unit: str | None
    desc: str | None
    value: list | None
    default: str | int | float | list | dict | None = None
    required: bool = True

class DataModel(BaseModel):
    name: str
    type: str
    desc: str | None = None

class ResultModel(BaseModel):
    name: str
    type: str
    desc: str | None = None

class AlgorithmModel(BaseModel):
    name: str
    desc: str
    args: list[ArgumentModel] | None = None
    data: list[DataModel] | None = None
    results: list[ResultModel] | None = None


class InfosRequest(RequestModel):
    name: str | list[str] | None = None

class InfosResponse(ResponseModel):
    result: list[AlgorithmModel] | AlgorithmModel | None = None

@router.post('/infos', response_model=InfosResponse, response_model_exclude_none=True)
async def infos(body: InfosRequest=Body()):
  if body.name and (type(body.name) is str):
      ret = AlgorithmManager.get(body.name)
      if ret:
        args: list[ArgumentModel] = []
        for a in ret.args:
            args.append(ArgumentModel(name=a.name,
                                      type=a.type,
                                      unit=a.unit,
                                      desc=a.desc,
                                      value=a.value,
                                      default=a.default,
                                      required=a.required))
        data: list[DataModel] = []
        for d in ret.data:
            data.append(DataModel(name=d.name,
                                    type=d.type,
                                    desc=d.desc))           
        results: list[ResultModel] = []
        for r in ret.results:
            results.append(ResultModel(name=r.name,
                                       type=r.type,
                                       desc=r.desc))

        return InfosResponse(result=AlgorithmModel(name=ret.name,
                                                   desc=ret.desc,
                                                   args=args,
                                                   data=data,
                                                   results=results))
      else:
        return InfosResponse(result=None)
  else:
      rs: list[ArgumentModel] = []
      rets = AlgorithmManager.get_list(body.name)
      for ret in rets:
        args: list[ArgumentModel] = []
        for a in ret.args:
            args.append(ArgumentModel(name=a.name,
                                      type=a.type,
                                      unit=a.unit,
                                      desc=a.desc,
                                      value=a.value,
                                      default=a.default,
                                      required=a.required))
        data: list[DataModel] = []
        for d in ret.data:
            data.append(DataModel(name=d.name,
                                  type=d.type,
                                  desc=d.desc))           
        results: list[ResultModel] = []
        for r in ret.results:
            results.append(ResultModel(name=r.name,
                                  type=r.type,
                                  desc=r.desc))

        rs.append(AlgorithmModel(name=ret.name,
                                desc=ret.desc,
                                args=args,
                                data=data,
                                results=results))
      return InfosResponse(result=rs)