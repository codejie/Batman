"""
股票三方数据接口
"""
from app.exception import AppException
from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Depends, Body, verify_token
from app.data.remote_api import stock_third as third
from app.routers.common_model import DataFrameSetModel
from app.utils import utils

router: APIRouter = APIRouter(prefix='/data/third/stock', tags=['data', 'stock', 'third'], dependencies=[Depends(verify_token)])

# class DataFrameSetModel(BaseModel):
#   columns: list[str]
#   data: list[list[str | int | float | datetime | date | None]]

"""
创新高
- symbol
  - 0:  "创月新高"
  - 1: "半年新高"
  - 2: "一年新高"
  - 3: "历史新高"
"""
class NewHighRequest(RequestModel):
  category: int = 0

class NewHighResponse(ResponseModel):
  result: DataFrameSetModel

@router.post('/new_high', response_model=NewHighResponse, response_model_exclude_none=True)
async def new_high(body: NewHighRequest=Body()):
  try:
    df = third.new_high(body.category)
    result = df.to_dict(orient='tight', index=False)
    return NewHighResponse(result=(DataFrameSetModel(
      columns=result['columns'],
      data=result['data']
    )))
  except Exception as e:
    raise AppException(e)  

"""
连续上涨
"""
class UptrendRequest(RequestModel):
  days: int = 0

class UptrendResponse(ResponseModel):
  result: DataFrameSetModel

@router.post('/uptrend', response_model=UptrendResponse, response_model_exclude_none=True)
async def uptrend(body: UptrendRequest=Body()):
  try:
    df = third.uptrend(body.days)
    result = df.to_dict(orient='tight', index=False)
    return UptrendResponse(result=(DataFrameSetModel(
      columns=result['columns'],
      data=result['data']
    )))
  except Exception as e:
    raise AppException(e) 
  
"""
持续放量
"""
class HighVolumeRequest(RequestModel):
  days: int = 0

class HighVolumeResponse(ResponseModel):
  result: DataFrameSetModel

@router.post('/high_volume', response_model=HighVolumeResponse, response_model_exclude_none=True)
async def high_volume(body: HighVolumeRequest=Body()):
  try:
    df = third.high_volume(body.days)
    result = df.to_dict(orient='tight', index=False)
    return HighVolumeResponse(result=(DataFrameSetModel(
      columns=result['columns'],
      data=result['data']
    )))
  except Exception as e:
    raise AppException(e)
  
"""
量价齐升
"""
class RiseVolumePriceRequest(RequestModel):
  days: int = 0

class RiseVolumePriceResponse(ResponseModel):
  result: DataFrameSetModel

@router.post('/rise_volume_price', response_model=RiseVolumePriceResponse, response_model_exclude_none=True)
async def rise_volume_price(body: RiseVolumePriceRequest=Body()):
  try:
    df = third.high_volume(body.days)
    result = df.to_dict(orient='tight', index=False)
    return RiseVolumePriceResponse(result=(DataFrameSetModel(
      columns=result['columns'],
      data=result['data']
    )))
  except Exception as e:
    raise AppException(e)
  
"""
涨停股池
"""
class LimitUpPoolRequest(RequestModel):
  date: str = None

class LimitUpPoolResponse(ResponseModel):
  result: DataFrameSetModel

@router.post('/limit_up_pool', response_model=LimitUpPoolResponse, response_model_exclude_none=True)
async def rise_volume_price(body: LimitUpPoolRequest=Body()):
  try:
    date = body.date if body.date else utils.date2String1(utils.find_last_non_weekend_date())
    df = third.limit_up_pool(date)
    result = df.to_dict(orient='tight', index=False)
    return LimitUpPoolResponse(result=(DataFrameSetModel(
      columns=result['columns'],
      data=result['data']
    )))
  except Exception as e:
    raise AppException(e)  