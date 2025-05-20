from typing import List, Optional
from fastapi import APIRouter, Depends, WebSocket
from app.database import customized as db
from app.database.data.define import SpotData
from app.routers.common import DEFAULT_UID, RequestModel, ResponseModel, verify_token

router: APIRouter = APIRouter(prefix="/customized", tags=["customized"], dependencies=[Depends(verify_token)])

class CreateRequest(RequestModel):
  type: int
  code: str
  comment: Optional[str] = None

class CreateResponse(ResponseModel):
  result: int

@router.post('/create', response_model=CreateResponse)
async def create(request: CreateRequest):
  try:
    result = db.insert(uid=DEFAULT_UID, type=request.type, code=request.code, comment=request.comment)
    return CreateResponse(result=result)
  except Exception as e:
    raise e

class RecordsRequest(RequestModel):
  type: Optional[int] = None
  code: Optional[str] = None

class RecordsResponse(ResponseModel):
  result: List[db.CustomizedRecord] = []

@router.post('/records', response_model=RecordsResponse)
async def records(request: RecordsRequest):
  result = db.records(uid=DEFAULT_UID, type=request.type, code=request.code)
  return RecordsResponse(result=result)

class RemoveRequest(RequestModel):
  id: int

class RemoveResponse(ResponseModel):
  result: int

@router.post('/remove', response_model=RemoveResponse)
async def remove(request: RemoveRequest):
  result = db.delete(uid=DEFAULT_UID, id=request.id)
  return RemoveResponse(result=result)

class UpdateCommentRequest(RequestModel):
  id: int
  comment: Optional[str] = None

class UpdateCommentResponse(ResponseModel):
  result: int

@router.post('/update_comment', response_model=UpdateCommentResponse)
async def update_comment(request: UpdateCommentRequest):
  result = db.update_comment(uid=DEFAULT_UID, id=request.id, comment=request.comment)
  return UpdateCommentResponse(result=result)

class UpdateTargetRequest(RequestModel):
  id: int
  target: Optional[float] = None

class UpdateTargetResponse(ResponseModel):
  result: int

@router.post('/update_target', response_model=UpdateTargetResponse)
async def update_target(request: UpdateTargetRequest):
  result = db.update_target(uid=DEFAULT_UID, id=request.id, target=request.target)
  return UpdateTargetResponse(result=result)

class UpdateOrderRequest(RequestModel):
  id: int
  order: Optional[int] = 0

class UpdateOrderResponse(ResponseModel):
  result: int

@router.post('/update_order', response_model=UpdateOrderResponse)
async def update_order(request: UpdateOrderRequest):
  result = db.update_order(uid=DEFAULT_UID, id=request.id, order=request.order)
  return UpdateOrderResponse(result=result)
