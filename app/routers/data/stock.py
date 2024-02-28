"""
股票数据相关API
"""

from fastapi import APIRouter, Depends, Body

from ...dependencies import verify_token
from ...models.data import stock as model
from ...libs.data import stock as lib

from ... import logger

router = APIRouter(prefix='/data/stock', tags=['data', 'stock'], dependencies=[Depends(verify_token)])

@router.post('/individual_info', response_model=model.IndividualInfoResponse, response_model_exclude_unset=True)
async def individual_info(body: model.IndividualInfoRequest = Body()):
    result = lib.get_individual_info(symbol=body.symbol)
    # logger.debug(result)
    return model.IndividualInfoResponse(code=0, result=result.to_dict())

@router.post('/history', response_model=model.HistoryResponse, response_model_exclude_unset=True)
async def history(body: model.HistoryRequest = Body()):
    result = lib.get_history(
        symbol=body.symbol,
        start_date=body.start.strftime('%Y%m%d'),
        end_date=body.end.strftime('%Y%m%d'),
        period=body.peroid or 'daily'
        )
    return model.HistoryResponse(code=0, result=result.to_dict())