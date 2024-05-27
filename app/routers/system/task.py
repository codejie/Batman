"""
定时任务接口
"""
from fastapi import APIRouter, Depends, Body
from app.routers.dependencies import verify_admin
from app.routers.define import BaseModel, RequestModel, ResponseModel
from app.task_manager import taskManager

router = APIRouter(prefix='/sys/task', tags=['sys'], dependencies=[Depends(verify_admin)])

"""
获取任务Job信息
"""
class JobsRequest(RequestModel):
    id: str | None = None

class JobResponse(BaseModel):
    id: str
    trigger: str
    next_run: str

class JobsResponse(ResponseModel):
    result: list[JobResponse]

@router.post('/jobs', response_model=JobsResponse, response_model_exclude_unset=True)
async def jobs(body: JobsRequest=Body()):
    results: list[JobResponse] = []
    jobs = taskManager.get_jobs()
    for job in jobs:
        if body.id and body.id != job['id']:
            continue
        results.append(JobResponse(id=job['id'], trigger=job['trigger'], next_run=job['next run at']))
    return JobsResponse(result=results)