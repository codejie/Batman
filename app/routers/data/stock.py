"""
股票数据相关API
"""

from fastapi import APIRouter, Depends, Body
from typing import Dict, List
from pydantic.fields import Field
import datetime

from ..dependencies import verify_token
from .. import RequestModel, ResponseModel
from ...data import stock as ds

from ... import logger

router = APIRouter(prefix='/data/stock', tags=['data', 'stock'], dependencies=[Depends(verify_token)])

"""
股票个股信息接口
"""
class IndividualInfoRequest(RequestModel):
    symbol: str

class IndividualInfoResponse(ResponseModel):
    result: Dict | None = None


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
    # logger.debug(body.period)
    result = ds.get_history(
            symbol=body.symbol,
            start_date=body.start.strftime('%Y%m%d'),
            end_date=body.end.strftime('%Y%m%d'),
            # period=("daily" if body.period is None else body.period)
            period=(body.period or "daily"),
            adjust=(body.adjust or "")
        )
    # result = adapter.history(result)
    return HistoryResponse(code=0, result=result.to_dict('list'))

"""
股票实时数据接口
"""
class SpotRequest(RequestModel):
    symbols: List[str] | None = None

class SpotResponse(ResponseModel):
    result: Dict | None = None

@router.post('/spot', response_model=SpotResponse, response_model_exclude_unset=True)
async def spot(body: SpotRequest=Body()):
    result = ds.get_spot(body.symbols)
    logger.debug(f'\n{result}')
    return SpotResponse(result=result.to_dict('list'))