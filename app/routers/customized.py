
from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Body, Depends, verify_token
from app.database import customized

router: APIRouter = APIRouter(prefix='/customized', tags=['customized'], dependencies=[Depends(verify_token)])

"""
Common Model
"""
class DataModel(BaseModel):
  date: str
  price: float
  percentage: float
  amount: float
  volatility: float
  open: float
  close: float
  high: float
  low: float
  volume: int
  turnover: float
  rate: float 

"""
create
"""
class CreateRequest(RequestModel):
  type: int = 1
  code: str
  comment: str | None = None    

class CreateResponse(ResponseModel):
  pass

@router.post('/create', response_model=CreateResponse)
async def create(body: CreateRequest=Body()):
  uid = 99
  customized.insert(uid=uid, code=body.code, type=body.type, comment=body.comment)
  return CreateResponse(code=0)

"""
infos
"""
class InfosRequest(RequestModel):
  type: int | None = None
  with_data: bool = True
  date: str | None = None

class InfoModel(BaseModel):
  id: int
  code: str
  name: str
  type: int
  comment: str | None = None
  updated: str
  data:DataModel | None = None

class InfosResponse(ResponseModel):
  result: list[InfoModel]

@router.post('/infos', response_model=InfosResponse, response_model_exclude_unset=True)
async def infos(body: InfosRequest=Body()):
  ret = customized.get_list(uid=99)
  print(ret)
  return InfosResponse(result=ret)