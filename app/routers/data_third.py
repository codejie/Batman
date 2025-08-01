"""
股票三方数据接口
"""
from datetime import datetime, date
from typing import Optional
import json

from fastapi import APIRouter, Body, Depends
import numpy as np
from pydantic import BaseModel
from app.exception import AppException
from app.database.data.third import stock as third
from app.routers.common import RequestModel, ResponseModel, verify_token

router: APIRouter = APIRouter(prefix='/data/third', tags=['data', 'stock', 'third'], dependencies=[Depends(verify_token)])

class DataFrameSetModel(BaseModel):
  columns: list[str]
  data: list[list[str | int | float | datetime | date | None]]

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

@router.post('/stock/new_high', response_model=NewHighResponse, response_model_exclude_none=True)
async def new_high(body: NewHighRequest=Body()):
  try:
    df = third.new_high(body.category)
    result = df.replace({np.nan: None}).to_dict(orient='tight', index=False)
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

@router.post('/stock/uptrend', response_model=UptrendResponse, response_model_exclude_none=True)
async def uptrend(body: UptrendRequest=Body()):
  try:
    df = third.uptrend(body.days)
    result = df.replace({np.nan: None}).to_dict(orient='tight', index=False)
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

@router.post('/stock/high_volume', response_model=HighVolumeResponse, response_model_exclude_none=True)
async def high_volume(body: HighVolumeRequest=Body()):
  try:
    # df = third.high_volume(body.days)
    df = third.high_volume(body.days)
    result = df.replace({np.nan: None}).to_dict(orient='tight', index=False)
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

@router.post('/stock/rise_volume_price', response_model=RiseVolumePriceResponse, response_model_exclude_none=True)
async def rise_volume_price(body: RiseVolumePriceRequest=Body()):
  try:
    # df = third.rise_volume_price(body.days)result = df.replace({np.nan: None}).to_dict(orient='tight', index=False)
    df = third.rise_volume_price(body.days)
    result = df.replace({np.nan: None}).to_dict(orient='tight', index=False)
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
  date: str | None = None

class LimitUpPoolResponse(ResponseModel):
  result: DataFrameSetModel

@router.post('/stock/limit_up_pool', response_model=LimitUpPoolResponse, response_model_exclude_none=True)
async def limit_up_pool(body: LimitUpPoolRequest=Body()):
  try:
    df = third.limit_up_pool(body.date)
    result = df.replace({np.nan: None}).to_dict(orient='tight', index=False)
    return LimitUpPoolResponse(result=(DataFrameSetModel(
      columns=result['columns'],
      data=result['data']
    )))
  except Exception as e:
    raise AppException(e)
  
"""
Info Links
"""
class InfoLinksRequest(RequestModel):
  flag: Optional[int] = None

class LinkInfo(BaseModel):
  title: str
  url: str
  tip: Optional[str] = None
  needCode: Optional[bool] = False
  inWindow: Optional[bool] = False

class GroupInfo(BaseModel):
  title: str
  icon: str
  links: list[LinkInfo]

class InfoLinksResponse(ResponseModel):
  result: list[GroupInfo]

@router.post('/info/links', response_model=InfoLinksResponse, response_model_exclude_none=True)
async def info_links(body: InfoLinksRequest=Body()):
  with open('./app/routers/assets/info_links.json', 'r', encoding='utf-8') as f:
    links = json.load(f)
  result = [GroupInfo.model_validate(item) for item in links]
  return InfoLinksResponse(result=result)