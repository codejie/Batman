from datetime import datetime
from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Body, Depends, verify_token
from app.database import customized, stock

router: APIRouter = APIRouter(prefix='/customized', tags=['customized'], dependencies=[Depends(verify_token)])

"""
Common Model
"""
# class DataModel(BaseModel):
#   date: str
#   price: float
#   percentage: float
#   amount: float
#   volatility: float
#   open: float
#   close: float
#   high: float
#   low: float
#   volume: int
#   turnover: float
#   rate: float 

"""
create
"""
class CreateRequest(RequestModel):
  type: int = 1
  code: str
  comment: str | None = None    

class CreateResponse(ResponseModel):
  result: bool

@router.post('/create', response_model=CreateResponse, response_model_exclude_none=True)
async def create(body: CreateRequest=Body()):
  uid = 99
  found = customized.find(uid=uid, code=body.code, type=body.type)
  if not found:
    customized.insert(uid=uid, code=body.code, type=body.type, comment=body.comment)
    return CreateResponse(code=0, result=True)
  else:
    return CreateResponse(code=-1, message=f'{body.code} existed in comstomized list.', result=False)

"""
infos
"""
class InfosRequest(RequestModel):
  type: int | None = None
  # with_data: bool = True
  # date: str | None = None

class InfoModel(BaseModel):
  id: int
  code: str
  name: str
  type: int
  comment: str | None = None
  updated: datetime
  # data:DataModel | None = None

class InfosResponse(ResponseModel):
  result: list[InfoModel]

@router.post('/infos', response_model=InfosResponse, response_model_exclude_none=True)
async def infos(body: InfosRequest=Body()):
  uid = 99 # get_uid_by_token()
  ret: list[InfoModel] = customized.get_list(uid=uid, type=body.type)
  return InfosResponse(result=ret)

"""
Remove
"""
class RemoveRequest(RequestModel):
  id: int

class RemoveResponse(ResponseModel):
  result: int

@router.post('/remove', response_model=RemoveResponse, response_model_exclude_none=True)
async def remove(body: RemoveRequest=Body()):
  id = customized.delete(id=body.id)
  return RemoveResponse(result=id)
