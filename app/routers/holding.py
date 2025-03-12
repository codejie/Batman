from fastapi import APIRouter, Depends
from app.database import holding as db
from app.routers.common import DEFAULT_UID, RequestModel, ResponseModel, verify_token

router: APIRouter = APIRouter(prefix="/holding", tags=["Holding"], dependencies=[Depends(verify_token)])

class CreateRequest(RequestModel):
    # uid: int
    type: int = None
    code: str = None
    flag: int = None

class CreateResponse(ResponseModel):
  result: int

@router.post("/create", response_model=CreateResponse)
async def create(request: CreateRequest):
  result = db.insert_holding(DEFAULT_UID, request.type, request.code)
  return CreateResponse(result=result)