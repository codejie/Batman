"""
股票数据相关API
"""

from fastapi import APIRouter, Depends, Body
# from typing import Dict, List
import pandas
from pydantic.fields import Field
from pydantic import BaseModel
import datetime

from app.routers.dependencies import verify_token
from app.routers.define import RequestModel, ResponseModel
from app.data import stock as ds
from app.toolkit.talib import overlap_studies as ta

from ... import logger

router = APIRouter(prefix='/data/stock', tags=['data', 'stock'], dependencies=[Depends(verify_token)])

"""
股票个股信息接口
"""
class IndividualInfoRequest(RequestModel):
    symbol: str

class IndividualInfoResponse(ResponseModel):
    result: dict | None = None


@router.post('/individual_info', response_model=IndividualInfoResponse, response_model_exclude_unset=True)
async def individual_info(body: IndividualInfoRequest = Body()):
    result = ds.get_individual_info(symbol=body.symbol)
    # logger.debug(result)
    return IndividualInfoResponse(code=0, result=result.to_dict('list'))

"""
股票历史数据接口
"""
class HistoryRequest(RequestModel):
    symbol: str
    start: datetime.date
    end: datetime.date
    period: str | None = Field(default="daily", description="daily/weekly/monthly")
    adjust: str | None = ""

class HistoryResponse(ResponseModel):
    result: dict | None = None
    
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
    # logger.debug(body.period)
    result = ds.get_history(
            symbol=body.symbol,
            start_date=body.start, # .strftime('%Y%m%d'),
            end_date=body.end, #.strftime('%Y%m%d'),
            # period=("daily" if body.period is None else body.period)
            period=(body.period or "daily"),
            adjust=(body.adjust or "qfq")
        )
    # result = adapter.history(result)
    return HistoryResponse(code=0, result=result.to_dict('list'))

"""
股票实时数据接口
"""
class SpotRequest(RequestModel):
    symbols: list[str] | None = None

class SpotResponse(ResponseModel):
    result: dict | None = None

@router.post('/spot', response_model=SpotResponse, response_model_exclude_unset=True)
async def spot(body: SpotRequest=Body()):
    result = ds.get_spot(body.symbols)
    logger.debug(f'\n{result}')
    return SpotResponse(result=result.to_dict('list'))

"""
股票历史数据MA接口
"""
class MAParameter(BaseModel):
    columns: list[str] | None = Field(default=None, description='需要处理的数据集合列名')
    periods: list[int] | None = Field(default=[5], description='MA分析周期，支持多个周期')
    types: list[str] | None = Field(default=['SMA'], description='MA类型：SMA/EMA/WMA/DEMA/TEMA/TRIMA/KAMA/MAMA/T3')
                                    
class HistoryMARequest(RequestModel):
    history_param: HistoryRequest
    ma_param: MAParameter

class HistoryMAResponse(ResponseModel):
    result: dict | None = Field(default=None, description='结果集合，包括历史数据列以及MA结果列，其列名格式为：{col}_{type}{period}')

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

