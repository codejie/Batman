import datetime
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.database.funds import FUNDS_STOCK
from app.routers.common import DEFAULT_UID, RequestModel, ResponseModel, verify_token
from app.database import funds as db


router: APIRouter = APIRouter(prefix="/funds", tags=["Funds"], dependencies=[Depends(verify_token)])

# class CreateRequest(RequestModel):
#   type: Optional[int] = FUNDS_STOCK
#   amount: float

# class CreateResponse(ResponseModel):
#   result: int

# @router.post('/create', response_model=CreateResponse)
# async def create(request: CreateRequest):
#   result = db.insert(uid=DEFAULT_UID, type=request.type, amount=request.amount)
#   return CreateResponse(result=result)

class GetRequest(RequestModel):
  type: Optional[int] = FUNDS_STOCK

class FundsTableModel(BaseModel):
  id: int
  type: int
  amount: float
  available: Optional[float] = None
  updated: datetime.datetime

class GetResponse(ResponseModel):
  result: Optional[FundsTableModel] = None

@router.post('/get', response_model=GetResponse)
async def get(request: GetRequest):
  result = db.get(uid=DEFAULT_UID, type=request.type)
  if result is None:
    return GetResponse(result=None)
  return GetResponse(result=FundsTableModel(id=result.id, type=result.type, amount=result.amount, available=result.available, updated=result.updated))

class UpdateRequest(RequestModel):
  type: Optional[int] = FUNDS_STOCK
  amount: float
  comment: Optional[str] = None

class UpdateResponse(ResponseModel):
  result: int

@router.post('/update', response_model=UpdateResponse)
async def update(request: UpdateRequest):
  result = db.update_funds(uid=DEFAULT_UID, type=request.type, amount=request.amount, comment=request.comment)
  return UpdateResponse(result=result)

# class OperationCreateRequest(RequestModel):
#   funds: int
#   # action: int
#   amount: float
#   comment: Optional[str]

# class OperationCreateResponse(ResponseModel):
#   result: int

# @router.post('/operation/create', response_model=OperationCreateResponse)
# async def operation(request: OperationCreateRequest):
#   # amount = request.amount if request.action == OPERATION_ACTION_IN else -request.amount
#   result = db.insert_operation(funds=request.funds, action=request.action, amount=request.amount, comment=request.comment)
#   # funds = db.get(request.funds)
#   # amount = funds.amount + amount
#   db.update(uid=DEFAULT_UID, id=request.funds, amount=request.amount)
#   return OperationCreateResponse(result=result)

class GetOperationRequest(RequestModel):
  funds: int

class OperationTableModel(BaseModel):
  id: int
  funds: int
  action: int
  amount: float
  comment: Optional[str] = None
  create: datetime.datetime

class GetOperationResponse(ResponseModel):
  result: Optional[OperationTableModel] = []

@router.post('/operation/get', response_model=GetOperationResponse)
async def get(request: GetOperationRequest):
  ret = db.get_operation(funds=request.funds)
  result = []
  for r in ret:
    result.append(OperationTableModel(id=r.id, funds=r.funds, action=r.action, amount=r.amount, comment=r.comment, create=r.created))
  return GetOperationResponse(result=result)