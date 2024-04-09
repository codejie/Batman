"""
持久化数据接口
"""
from fastapi import APIRouter, Depends, Body

from app.routers.dependencies import verify_admin
from app.routers.define import RequestModel, ResponseModel
# from app.scheduler import scheduler
from app.task_manager import taskManager
from app.data.local_db import stock

router = APIRouter(prefix='/sys/data/stock', tags=['sys'], dependencies=[Depends(verify_admin)])

JOB_DELAY_SECONDS = 2

"""
下载A股信息列表
"""
class FetchAListRequest(RequestModel):
    if_exists: str = 'replace'

class FetchAListResponse(ResponseModel):
    result: str

@router.post('/fetch_a_list', response_model=FetchAListResponse, response_model_exclude_unset=True)
def fetch_a_list(body: FetchAListRequest=Body()):
    # id = scheduler.addDelayJob(stock.fetch_a_stock, body.model_dump(), seconds=JOB_DELAY_SECONDS)
    id = taskManager.create_fetch_data(stock.fetch_a_stock, body.model_dump(), seconds=JOB_DELAY_SECONDS)
    return FetchAListResponse(result=id)

"""
下载A股列表中股票历史数据任务
"""
class FetchHistoryRequest(RequestModel):
    symbol: str | None = None
    start: str
    end: str
    period: str = 'daily'
    adjust: str = 'qfq'
    if_exists: str = 'replace'

class FetchHistoryResponse(ResponseModel):
    result: str

@router.post('/fetch_history', response_model=FetchHistoryResponse, response_model_exclude_unset=True)
def fetch_history(body: FetchHistoryRequest=Body()):
    # id = scheduler.addDelayJob(stock.fetch_history, body.model_dump(), JOB_DELAY_SECONDS)
    id = taskManager.create_fetch_data(stock.fetch_history, body.model_dump(), JOB_DELAY_SECONDS)
    return FetchHistoryResponse(result=id)

"""
下载A股列表中股票个股持股数据
"""
class FetchHSGTRequest(RequestModel):
    symbol: str | None = None
    if_exists: str = 'replace'

class FetchHSGTResponse(ResponseModel):
    result: str

@router.post('/fetch_hsgt', response_model=FetchHSGTResponse, response_model_exclude_unset=True)
def fetch_hsgt(body: FetchHSGTRequest=Body()):
    # id = scheduler.addDelayJob(stock.fetch_hsgt, body.model_dump(), JOB_DELAY_SECONDS)
    id = taskManager.create_fetch_data(stock.fetch_hsgt, body.model_dump(), JOB_DELAY_SECONDS)
    return FetchHSGTResponse(result=id)

"""
下载A股列表中股票个股融资融券数据
"""
class FetchMarginRequest(RequestModel):
    symbol: str | None = None
    start: str
    end: str
    if_exists: str = 'append'

class FetchMarginResponse(ResponseModel):
    result: str

@router.post('/fetch_margin', response_model=FetchMarginResponse, response_model_exclude_unset=True)
def fetch_margin(body: FetchMarginRequest=Body()):
    # id = scheduler.addDelayJob(stock.fetch_margin, body.model_dump(), JOB_DELAY_SECONDS)
    id = taskManager.create_fetch_data(stock.fetch_margin, body.model_dump(), JOB_DELAY_SECONDS)
    return FetchMarginResponse(result=id)