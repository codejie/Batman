from typing import List, Optional
from fastapi import APIRouter, Depends
from app.database import holding as db
from app.routers.common import DEFAULT_UID, RequestModel, ResponseModel, verify_token

router: APIRouter = APIRouter(prefix="/holding", tags=["Holding"], dependencies=[Depends(verify_token)])

# class CreateRequest(RequestModel):
#     # uid: int
#     type: int
#     code: str
#     action: int
#     quantity: int
#     price: float
#     expense: float
#     comment: Optional[str] = None

# class CreateResponse(ResponseModel):
#   result: int

# @router.post("/create", response_model=CreateResponse)
# async def create(request: CreateRequest):
#   result = db.create(uid=DEFAULT_UID,
#                      type=request.type,
#                      code=request.code,
#                      action=request.action,
#                      quantity=request.quantity,
#                      price=request.price,
#                      expense=request.expense,
#                      comment=request.comment)
#   return CreateResponse(result=result)

class CreateRequest(RequestModel):
  type: int
  code: str
  flag: Optional[int] = None

class CreateResponse(ResponseModel):
  result: int

@router.post('/create', response_model=CreateResponse)
async def create(request: CreateRequest):
  result = db.insert_holding(uid=DEFAULT_UID, type=request.type, code=request.code)
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

class RemoveRequest(RequestModel):
  id: int

class RemoveResponse(ResponseModel):
  result: int

@router.post("/remove", response_model=RemoveResponse)
async def remove(request: RemoveRequest):
  result = db.update_holding_flag(uid=DEFAULT_UID, id=request.id, flag=db.HOLDING_FLAG_REMOVED)
  return RemoveResponse(result=result)

class OperationRequest(RequestModel):
  holding: int
  action: int
  quantity: int
  price: float
  expense: Optional[float] = None
  comment: Optional[str] = None

class OperationResponse(ResponseModel):
  result: int

@router.post("/operation", response_model=OperationResponse)
async def operation(request: OperationRequest):
  if request.expense is None:
    request.expense = request.price * request.quantity
  result = db.insert_operation(id=request.holding, action=request.action, quantity=request.quantity, price=request.price, expense=request.expense, comment=request.comment)
  return OperationResponse(result=result)

class RecordRequest(RequestModel):
  type: Optional[int] = None
  code: Optional[str] = None
  flag: Optional[int] = db.HOLDING_FLAG_ACTIVE

class RecordResponse(ResponseModel):
  result: List[db.UserHoldingRecord] = []

@router.post("/record", response_model=RecordResponse)
async def record(request: RecordRequest):
  result = db.records(uid=DEFAULT_UID, type=request.type, code=request.code, flag=request.flag)
  return RecordResponse(result=result)