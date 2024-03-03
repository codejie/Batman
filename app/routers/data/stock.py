"""
股票数据相关API
"""

from fastapi import APIRouter, Depends, Body

from ..dependencies import verify_token
from . import models
from ...data import stock as ds

from ... import logger

router = APIRouter(prefix='/data/stock', tags=['data', 'stock'], dependencies=[Depends(verify_token)])

@router.post('/individual_info', response_model=models.IndividualInfoResponse, response_model_exclude_unset=True)
async def individual_info(body: models.IndividualInfoRequest = Body()):
    result = ds.get_individual_info(symbol=body.symbol)
    # logger.debug(result)
    return models.IndividualInfoResponse(code=0, result=result.to_dict('list'))

@router.post('/history', response_model=models.HistoryResponse, response_model_exclude_unset=True)
async def history(body: models.HistoryRequest = Body()):
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
        period=(body.period or "daily")
        )
    # result = adapter.history(result)
    return models.HistoryResponse(code=0, result=result.to_dict('list'))

@router.post('/spot', response_model=models.SpotResponse, response_model_exclude_unset=True)
async def spot(body: models.SpotRequest=Body()):
    result = ds.get_spot(body.symbols)
    logger.debug(f'\n{result}')
    return models.SpotResponse(result=result.to_dict('list'))