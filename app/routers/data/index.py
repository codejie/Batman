"""
股票指数相关API
"""

from typing import Dict, List
import pandas
from pydantic import BaseModel
from pydantic.fields import Field
import datetime
from fastapi import APIRouter, Depends, Body

from app.routers.dependencies import verify_token
from app.routers.define import RequestModel, ResponseModel
from app.data.remote_api import index as ds
from app.toolkit.talib import overlap_studies as ta

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

"""
指数历史数据MA接口
"""
class MAParameter(BaseModel):
    columns: List[str] | None = Field(default=None, description='需要处理的数据集合列名')
    periods: List[int] | None = Field(default=[5], description='MA分析周期，支持多个周期')
    types: List[str] | None = Field(default=['SMA'], description='MA类型：SMA/EMA/WMA/DEMA/TEMA/TRIMA/KAMA/MAMA/T3')
                                    
class HistoryMARequest(RequestModel):
    history_param: HistoryRequest
    ma_param: MAParameter

class HistoryMAResponse(ResponseModel):
    result: Dict | None = Field(default=None, description='结果集合，包括历史数据列以及MA结果列，其列名格式为：{col}_{type}{period}')

@router.post('/history_ma_turbo', response_model=HistoryMAResponse, response_model_exclude_unset=True)
async def history_ma_turbo(body: HistoryMARequest=Body()):
    df = ds.get_history(
            symbol=body.history_param.symbol,
            start_date=body.history_param.start.strftime('%Y%m%d'),
            end_date=body.history_param.end.strftime('%Y%m%d'),
            period=(body.history_param.period or "daily"),
            adjust=(body.history_param.adjust or "")
    )
    result = pandas.concat([df, ta.MA_turbo(
        df=df,
        columns=body.ma_param.columns,
        periods=body.ma_param.periods,
        types=body.ma_param.types)], axis=1)
    return HistoryMAResponse(result=result.to_dict('list'))