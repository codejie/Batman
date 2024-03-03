"""
股票指数相关API
"""

from fastapi import APIRouter, Depends, Body

from ..dependencies import verify_token
from . import models
from ...data import index as ds

router = APIRouter(prefix='/data/index', tags=['data', 'index'], dependencies=[Depends(verify_token)])

@router.post('/infos', response_model=models.InfosResponse, response_model_exclude_unset=True)
async def individual_info(body: models.InfosRequest = Body()):
    result = ds.get_infos()
    return models.InfosResponse(code=0, result=result.to_dict('list'))

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
    result = ds.get_history(
        symbol=body.symbol,
        start_date=body.start.strftime('%Y%m%d'),
        end_date=body.end.strftime('%Y%m%d'),
        period=(body.period or "daily")
        )
    return models.HistoryResponse(code=0, result=result.to_dict('list'))
