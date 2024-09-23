from datetime import datetime
from app.database import holding
from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Body, Depends, verify_token

router: APIRouter = APIRouter(prefix='/holding', tags=['holding'], dependencies=[Depends(verify_token)])

"""
insert
"""
class CreateRequest(RequestModel):
  type: int
  code: str
  quantity: int
  deal: float
  cost: float
  comment: str | None = None

class CreateResponse(ResponseModel):
  result: int

@router.post('/create', response_model=CreateResponse, response_model_exclude_none=True)
async def create(body: CreateRequest=Body()):
  uid = 99
  result = holding.insert(uid, body.type, body.code, body.quantity, body.deal, body.cost, body.comment)
  return CreateResponse(result=result)

"""
Update
"""
class UpdateRequest(RequestModel):
  action: int
  type: int
  code: str
  quantity: int
  deal: float
  cost: float
  comment: str | None = None

class UpdateResponse(ResponseModel):
  result: int

@router.post('/update', response_model=UpdateResponse, response_model_exclude_none=True)
async def update(body: UpdateRequest=Body()):
  uid = 99
  result = holding.update(uid, body.action, body.type, body.code, body.quantity, body.deal, body.cost, body.comment)
  return UpdateResponse(result=result)

"""
Remove
"""
class RemoveRequest(RequestModel):
  id: int

class RemoveResponse(ResponseModel):
  result: int

@router.post('/remove', response_model=RemoveResponse, response_model_exclude_none=True)
async def remove(body: RemoveRequest=Body()):
  uid = 99
  result = holding.remove(uid, body.id)
  return RemoveResponse(result=result)

"""
GetHoldingList
"""
class GetHoldingListResquest(RequestModel):
  type: int | None = None
  code: str | None = None
  with_removed: bool = False

class HoldingModel(BaseModel):
  id: int
  type: int
  code: str
  name: str
  created: datetime
  updated: datetime
  flag: int

class GetHoldingListResponse(ResponseModel):
  result: list[HoldingModel]

@router.post('get_holding', response_model=GetHoldingListResponse, response_model_exclude_none=True)
async def get_holding(body: GetHoldingListResquest=Body()):
  uid = 99
  result = holding.get_holding(uid, body.type, body.code, body.with_removed)
  return GetHoldingListResponse(result=result)

"""
GetRecordList
"""
class GetRecordListResquest(RequestModel):
  holding: int | None = None
  action: int | None = None
  with_removed: bool = False

class RecordModel(BaseModel):
  id: int
  holding: int
  action: int
  quantity: int
  deal: float
  cost: float
  comment: str | None
  created: datetime

class GetRecordListResponse(ResponseModel):
  result: list[RecordModel]

@router.post('get_record', response_model=GetRecordListResponse, response_model_exclude_none=True)
async def get_record(body: GetRecordListResquest=Body()):
  uid = 99
  result = holding.get_record(uid, body.holding, body.action, body.with_removed)
  return GetRecordListResponse(result=result)