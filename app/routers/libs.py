from fastapi import APIRouter, Body, Depends
from pandas import Series
from app.libs.talib.momentum_indicators import MACD
from app.routers.common import RequestModel, ResponseModel, verify_token
from app.routers.data_third_stock import DataFrameSetModel

router = APIRouter(prefix='/libs/talib', tags=['libs', 'talib'], dependencies=[Depends(verify_token)])

"""
MACD
"""
class MACDRequest(RequestModel):
  value: dict | list[float]
  fast: int = 12
  slow: int = 26
  period: int = 9

class MACDResponse(ResponseModel):
  result: DataFrameSetModel

@router.post('/macd', response_model=MACDResponse, response_model_exclude_none=True)
async def macd(body: MACDRequest=Body()):
  series = Series(body.value)
  # if type(body.value) == 'dict':
  #   series = Series(body.value)
  df = MACD(value=series, fast_period=body.fast, slow_period=body.slow, signal_period=body.period)
  df = df.fillna('-')
  result = df.to_dict(orient='tight', index=False)
  return MACDResponse(result=DataFrameSetModel(
    columns=result['columns'],
    data=result['data']
  ))
