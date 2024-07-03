from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Depends, Body, verify_admin_token
from app.task_scheduler import taskScheduler

router: APIRouter = APIRouter(prefix="/sys", tags=['system'], dependencies=[Depends(verify_admin_token)])

"""
Task's Jobs
"""
class JobsRequest(RequestModel):
  id: str | None = None

class JobsResponse(ResponseModel):
  result: list[dict]

@router.post('/jobs', response_model=JobsResponse, response_model_exclude_none=True)
async def jobs(body: JobsRequest=Body()):
  results = taskScheduler.jobs()
  return JobsResponse(result=results)