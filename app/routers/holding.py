import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.database import holding as db
from app.routers.common import DEFAULT_UID, RequestModel, ResponseModel, verify_token

router: APIRouter = APIRouter(prefix="/holding", tags=["Holding"], dependencies=[Depends(verify_token)])

class CreateRequest(RequestModel):
  type: int
  code: str
  flag: Optional[int] = db.HOLDING_FLAG_ACTIVE

class CreateResponse(ResponseModel):
  result: int

@router.post('/create', response_model=CreateResponse)
async def create(request: CreateRequest):
  result = db.insert_holding(uid=DEFAULT_UID, type=request.type, code=request.code, flag=request.flag)
  return CreateResponse(result=result)

class ListRequest(RequestModel):
  type: Optional[int] = None
  code: Optional[int] = None
  flag: Optional[int] = db.HOLDING_FLAG_ACTIVE

class ListResponse(ResponseModel):
   result: list[db.UserHoldingRecord] = []

@router.post("/list", response_model=ListResponse)
async def list(request: ListRequest):
  result = db.records(uid=DEFAULT_UID, type=request.type, code=request.code, flag=request.flag)
  return ListResponse(result=result)

class FlagRequest(RequestModel):
  id: int
  flag: Optional[int] = db.HOLDING_FLAG_REMOVED

class FlagResponse(ResponseModel):
  result: int

@router.post("/flag", response_model=FlagResponse)
async def remove(request: FlagRequest):
  result = db.update_holding_flag(uid=DEFAULT_UID, id=request.id, flag=request.flag)
  return FlagResponse(result=result)

class OperationCreateRequest(RequestModel):
  holding: int
  action: int
  quantity: int
  price: float
  expense: Optional[float] = None
  comment: Optional[str] = None

class OperationCreateResponse(ResponseModel):
  result: int

@router.post("/operation/create", response_model=OperationCreateResponse)
async def operation(request: OperationCreateRequest):
  if request.expense is None:
    request.expense = request.price * request.quantity
  result = db.insert_operation(id=request.holding, action=request.action, quantity=request.quantity, price=request.price, expense=request.expense, comment=request.comment)
  return OperationCreateResponse(result=result)

class RecordRequest(RequestModel):
  id: Optional[int] = None
  type: Optional[int] = None
  code: Optional[str] = None
  flag: Optional[int] = db.HOLDING_FLAG_ACTIVE

class RecordResponse(ResponseModel):
  result: List[db.UserHoldingRecord] = []

@router.post("/record", response_model=RecordResponse)
async def record(request: RecordRequest):
  result = db.records(uid=DEFAULT_UID, id=request.id, type=request.type, code=request.code, flag=request.flag)
  return RecordResponse(result=result)

class OperationListRequest(RequestModel):
  holding: Optional[int] = None

class HoldingOperationTableModel(BaseModel):
  id: int
  holding: int
  action: int
  quantity: int
  price: float
  expense: float
  comment: Optional[str] = None
  created: datetime.datetime

  class Config:
    from_attributes = True

class OperationListResponse(ResponseModel):
  result: List[HoldingOperationTableModel] = []

@router.post("/operation/list", response_model=OperationListResponse)
async def operation_list(request: OperationListRequest):
  records = db.select_operation(uid=DEFAULT_UID, holding=request.holding)
  results = []
  for record in records:
    r = record[0]
    results.append(HoldingOperationTableModel(id=r.id, holding=r.holding, action=r.action, quantity=r.quantity, price=r.price, expense=r.expense, comment=r.comment, created=r.created))
  # rows = db.select_operation(uid=DEFAULT_UID, holding=request.holding)
  # results = []
  # for row in rows:
  #   results.append(HoldingOperationTableModel.model_validate(row))
  return OperationListResponse(result=results)

class OperationRemoveRequest(RequestModel):
  id: int

class OperationRemoveResponse(ResponseModel):
  result: int

@router.post("/operation/remove", response_model=OperationRemoveResponse)
async def operation_remove(request: OperationRemoveRequest):
  result = db.delete_operation(uid=DEFAULT_UID, id=request.id)
  return OperationRemoveResponse(result=result)