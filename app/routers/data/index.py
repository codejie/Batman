"""
股票指数相关API
"""

from fastapi import APIRouter, Depends, Body

from ..dependencies import verify_token
from ..models.data import index as model
from ...datasource import index as ds

router = APIRouter(prefix='/data/index', tags=['data', 'index'], dependencies=[Depends(verify_token)])

@router.post('/infos', response_model=model.InfosResponse, response_model_exclude_unset=True)
async def individual_info(body: model.InfosRequest = Body()):
    result = ds.get_infos()
    return model.InfosResponse(code=0, result=result.to_dict('list'))

@router.post('/history', response_model=model.HistoryResponse, response_model_exclude_unset=True)
async def history(body: model.HistoryRequest = Body()):
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
    return model.HistoryResponse(code=0, result=result.to_dict('list'))
