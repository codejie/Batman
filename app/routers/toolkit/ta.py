"""
使用TA分析相关API
"""

from fastapi import APIRouter, Depends, Body
from pandas import DataFrame
from typing import Dict, List
from pydantic.fields import Field

from .. import RequestModel, ResponseModel
from ..dependencies import verify_token
from ...toolkit import adapter, ta

from ... import logger

router = APIRouter(prefix='/tool/ta', tags=['toolkit', 'ta'], dependencies=[Depends(verify_token)])

"""
MA方法接口定义
"""
class MARequest(RequestModel):
    ds: Dict = Field(description='数据集合')
    columns: List[str] | None = Field(default=None, description='需要处理的数据集合列名')
    periods: List[int] | None = Field(default=[5], description='MA分析周期，支持多个周期')
    types: List[str] | None = Field(default=['SMA'], description='MA类型：SMA/EMA/WMA/DEMA/TEMA/TRIMA/KAMA/MAMA/T3')

class MAResponse(ResponseModel):
    result: Dict | None = Field(default=None, description='结果集合，列名格式为：{col}_{type}{period}')

@router.post('/ma', response_model=MAResponse, response_model_exclude_unset=True)
async def ma(body: MARequest = Body()):
    df = DataFrame().from_dict(body.ds)
    # df = adapter.df_akshare2standard(df) # Shuld be removed when release.
    result = ta.MA(df, body.columns, body.periods, body.types)
    return MAResponse(result=result.to_dict('list'))

"""
BBANDS方法接口
"""
class BBANDSRequest(RequestModel):
    ds: Dict = Field(description='数据集合')
    columns: List[str] | None = Field(default=None, description='需要处理的数据集合列名')
    period: int | None = Field(default=5, description='分析周期')
    upper: int | None = Field(default=2, description='上轨线标准差倍数')
    lower: int | None = Field(default=2, description='下轨线标准差倍数')
    types: List[str] | None = Field(default=['SMA'], description='MA类型：SMA/EMA/WMA/DEMA/TEMA/TRIMA/KAMA/MAMA/T3')

class BBANDSResponse(ResponseModel):
    result: Dict | None = Field(default=None, description='结果集合，包括上轨数据{col}_upper、中轨数据{col}_middle、下柜数据{col}_lower')

@router.post('/bbands', response_model=BBANDSResponse, response_model_exclude_unset=True, response_model_exclude_none=True)
async def ma(body: BBANDSRequest = Body()):
    logger.debug(body.ds)
    logger.debug(type(body.ds))
    df = DataFrame().from_dict(body.ds)
    # df = adapter.df_akshare2standard(df) # Shuld be removed when release.
    logger.debug(df)
    result = ta.BBANDS(df, body.columns, body.period, body.upper, body.lower, body.types)
    return MAResponse(result=result.to_dict('list'))