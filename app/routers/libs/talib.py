from pandas import Series
from app.routers.definition import APIRouter, BaseModel, RequestModel, ResponseModel, Depends, Body, verify_token
from app.libs.talib.momentum_indicators import MACD
from app.routers.common_model import DataFrameSetModel


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
  print(body.value)
  series = Series(body.value)
  # if type(body.value) == 'dict':
  #   series = Series(body.value)
  print(series)
  df = MACD(value=series, fast_period=body.fast, slow_period=body.slow, signal_period=body.period)
  print(df)
  df = df.fillna('-')
  print(df)
  result = df.to_dict(orient='tight', index=False)
  print(result)
  return MACDResponse(result=DataFrameSetModel(
    columns=result['columns'],
    data=result['data']
  ))
