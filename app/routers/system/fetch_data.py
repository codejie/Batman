"""
持久化数据接口
"""
from fastapi import APIRouter, Depends, Body
import pandas

from app.routers.dependencies import verify_admin
from app.routers.define import RequestModel, ResponseModel
from app.scheduler import scheduler
from app.data.local_db import stock, index

router = APIRouter(prefix='/sys/data', tags=['sys'], dependencies=[Depends(verify_admin)])

JOB_DELAY_SECONDS = 2

"""
下载A股信息列表
"""
class FetchAStockListRequest(RequestModel):
    if_exists: str = 'replace'

class FetchAStockListResponse(ResponseModel):
    result: str

@router.post('/fetch_a_stock_list', response_model=FetchAStockListResponse, response_model_exclude_unset=True)
def fetch_a_stock_list(body: FetchAStockListRequest=Body()):
    id = scheduler.addDelayJob(stock.fetch_a_stock, body.model_dump(), seconds=JOB_DELAY_SECONDS)
    return FetchAStockListResponse(result=id)

"""
下载A股列表中股票历史数据任务
"""
class FetchStockHistoryRequest(RequestModel):
    symbol: str | None = None
    start: str
    end: str
    period: str = 'daily'
    adjust: str = 'qfq'
    if_exists: str = 'replace'

class FetchStockHistoryResponse(ResponseModel):
    result: str

@router.post('/fetch_stock_history', response_model=FetchStockHistoryResponse, response_model_exclude_unset=True)
def fetch_stock_history(body: FetchStockHistoryRequest=Body()):
    id = scheduler.addDelayJob(stock.fetch_all_history, body.model_dump(), JOB_DELAY_SECONDS)
    return FetchStockHistoryResponse(result=id)

"""
添加A股指数代码
"""
class AppendIndexCodeRequest(RequestModel):
    code: str
    name: str

class AppendIndexCodeResponse(ResponseModel):
    result: str

@router.post('/append_index_code', response_model=AppendIndexCodeResponse, response_model_exclude_unset=True)
def append_index_code(body: AppendIndexCodeRequest=Body()):
    id = scheduler.addDelayJob(index.append_a_index, body.model_dump(), JOB_DELAY_SECONDS)
    return AppendIndexCodeResponse(result=id)

"""
下载指数列表中指数历史数据
"""
class FetchIndexHistoryRequest(RequestModel):
    symbol: str | None = None
    start: str
    end: str
    period: str = 'daily'
    if_exists: str = 'replace'

class FetchIndexHistoryResponse(ResponseModel):
    result: str

@router.post('/fetch_index_history', response_model=FetchIndexHistoryResponse, response_model_exclude_unset=True)
def fetch_index_history(body: FetchIndexHistoryRequest=Body()):
    print(f'!!!!{body.model_dump()}')
    id = scheduler.addDelayJob(index.fetch_history, body.model_dump(), JOB_DELAY_SECONDS)
    return FetchIndexHistoryResponse(result=id)