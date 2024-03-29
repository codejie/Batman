"""
持久化数据接口
"""
from fastapi import APIRouter, Depends, Body
import pandas

from app.routers.dependencies import verify_admin
from app.routers.define import RequestModel, ResponseModel
from app.data.local_db.jobs import scheduleFetchJob

router = APIRouter(prefix='/sys/data', tags=['sys'], dependencies=[Depends(verify_admin)])

"""
下载A股信息列表
"""
class FetchAStockListRequest(RequestModel):
    pass

class FetchAStockListResponse(ResponseModel):
    result: str

@router.post('/fetch_a_stock_list', response_model=FetchAStockListResponse, response_model_exclude_unset=True)
async def fetch_a_stock_list(body: FetchAStockListRequest=Body):
    id = await scheduleFetchJob('fetch_a_stock')
    return FetchAStockListResponse(result=id)