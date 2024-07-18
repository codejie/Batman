from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Body, Depends, verify_token
from app.database import customized

router: APIRouter = APIRouter(prefix='/customized', tags=['customized'], dependencies=[Depends(verify_token)])

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