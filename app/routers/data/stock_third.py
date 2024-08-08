"""
股票三方数据接口
"""
from datetime import datetime, date
from app.exception import AppException
from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Depends, Body, verify_token
from app.data.remote_api import stock_third as third
from app.routers.common_model import DataFrameSetModel

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
