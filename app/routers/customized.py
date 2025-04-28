from typing import Optional
from fastapi import APIRouter, Depends
from app.database import customized as db
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
  result = db.insert(uid=DEFAULT_UID, type=request.type, code=request.code, comment=request.comment)
  return CreateResponse(result=result)

class RecordsRequest(RequestModel):
  type: Optional[int] = None
  code: Optional[str] = None

class RecordsResponse(ResponseModel):
  result: list[db.CustomizedRecord]

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
  result = db.update_comment(id=request.id, comment=request.comment)
  return UpdateCommentResponse(result=result)