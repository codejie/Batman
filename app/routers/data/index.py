"""
股票指数相关API
"""

from typing import Dict, List
from pydantic.fields import Field
import datetime
from fastapi import APIRouter, Depends, Body

from ..dependencies import verify_token
from .. import RequestModel, ResponseModel
from ...data import index as ds

router = APIRouter(prefix='/data/index', tags=['data', 'index'], dependencies=[Depends(verify_token)])

"""
指数信息接口
"""
class InfosRequest(RequestModel):
    pass

class InfosResponse(ResponseModel):
    result: Dict | None = None

@router.post('/infos', response_model=InfosResponse, response_model_exclude_unset=True)
async def individual_info(body: InfosRequest = Body()):
    result = ds.get_infos()
    return InfosResponse(code=0, result=result.to_dict('list'))

"""
指数历史数据接口
"""

class HistoryRequest(RequestModel):
    symbol: str
    start: datetime.date
    end: datetime.date
    period: str | None = Field(default="daily", description="daily/weekly/monthly")

class HistoryResponse(ResponseModel):
    result: Dict | None = None

@router.post('/history', response_model=HistoryResponse, response_model_exclude_unset=True)
async def history(body: HistoryRequest = Body()):
    """
    {
        "symbol": "002236",
        "start": "2023-01-01",
        "end": "2024-01-01",
        "period": "monthly"
    }
    """
    result = ds.get_history(
        symbol=body.symbol,
        start_date=body.start.strftime('%Y%m%d'),
        end_date=body.end.strftime('%Y%m%d'),
        period=(body.period or "daily")
        )
    return HistoryResponse(code=0, result=result.to_dict('list'))
