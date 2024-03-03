"""
使用TA分析相关API
"""

from fastapi import APIRouter, Depends, Body
from pandas import DataFrame
from ..dependencies import verify_token
from ...toolkit import adapter, ta
from . import models

from ... import logger

router = APIRouter(prefix='/tool/ta', tags=['toolkit', 'ta'], dependencies=[Depends(verify_token)])

@router.post('/ma', response_model=models.MAResponse, response_model_exclude_unset=True)
async def ma(body: models.MARequest = Body()):
    df = DataFrame().from_dict(body.ds)
    df = adapter.df_akshare2standard(df) # Shuld be removed when release.
    result = ta.MA(df, body.columns, body.periods, body.types)
    return models.MAResponse(result=result.to_dict('list'))

@router.post('/bbands', response_model=models.BBANDSResponse, response_model_exclude_unset=True, response_model_exclude_none=True)
async def ma(body: models.BBANDSRequest = Body()):
    logger.debug(body.ds)
    logger.debug(type(body.ds))
    df = DataFrame().from_dict(body.ds)
    df = adapter.df_akshare2standard(df) # Shuld be removed when release.
    logger.debug(df)
    result = ta.BBANDS(df, body.columns, body.period, body.upper, body.lower, body.types)
    return models.MAResponse(result=result.to_dict('list'))