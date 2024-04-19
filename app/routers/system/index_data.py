"""
持久化数据接口
"""
from fastapi import APIRouter, Depends, Body

from app.routers.dependencies import verify_admin
from app.routers.define import RequestModel, ResponseModel
# from app.scheduler import scheduler
from app.task_manager import taskManager
from app.data.local_db import index

router = APIRouter(prefix='/sys/data/index', tags=['sys'], dependencies=[Depends(verify_admin)])

JOB_DELAY_SECONDS = 2

"""
添加A股指数代码
"""
class AppendCodeRequest(RequestModel):
    code: str
    name: str

class AppendCodeResponse(ResponseModel):
    result: str

@router.post('/append_code', response_model=AppendCodeResponse, response_model_exclude_unset=True)
def append_index_code(body: AppendCodeRequest=Body()):
    # id = scheduler.addDelayJob(index.append_a_index, body.model_dump(), JOB_DELAY_SECONDS)
    id = taskManager.create_fetch_data(func=index.append_a_index, args=body.model_dump(), seconds=JOB_DELAY_SECONDS)
    return AppendCodeResponse(result=id)

"""
下载指数列表中指数历史数据
"""
class FetchHistoryRequest(RequestModel):
    symbol: str | None = None
    start: str
    end: str
    period: str = 'daily'
    if_exists: str = 'replace'

class FetchHistoryResponse(ResponseModel):
    result: str

@router.post('/fetch_history', response_model=FetchHistoryResponse, response_model_exclude_unset=True)
def fetch_index_history(body: FetchHistoryRequest=Body()):
    # id = scheduler.addDelayJob(index.fetch_history, body.model_dump(), JOB_DELAY_SECONDS)
    id = taskManager.create_fetch_data(index.fetch_history, body.model_dump(), JOB_DELAY_SECONDS)
    return FetchHistoryResponse(result=id)