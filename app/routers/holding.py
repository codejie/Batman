from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Body, Depends, verify_token

router: APIRouter = APIRouter(prefix='/holding', tags=['holding'], dependencies=[Depends(verify_token)])

"""
insert
"""
class InsertRequest(RequestModel):
  pass