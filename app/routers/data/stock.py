from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Depends, Body, verify_token
from pydantic.fields import Field
from pandas import DataFrame, Series
from datetime import datetime

from app.exception import AppException
from app.database import stock
router: APIRouter = APIRouter(prefix='/data/stock', tags=['data', 'stock'], dependencies=[Depends(verify_token)])

"""
Data Model
"""
class AListModel(BaseModel):
  code: str
  name: str

class HistoryDataModel(BaseModel):
  date: str
  price: float
  percentage: float
  amount: float
  volatility: float
  open: float
  close: float
  high: float
  low: float
  volume: int
  turnover: float
  rate: float

def history_data2model(row: Series) -> HistoryDataModel:
  return HistoryDataModel(
    date=row['日期'],
    price=row['收盘'],
    percentage=row['涨跌幅'],
    amount=row['涨跌额'],
    volatility=row['振幅'],
    open=row['开盘'],
    close=row['收盘'],
    high=row['最高'],
    low=row['最低'],
    volume=row['成交量'],
    turnover=row['成交额'],
    rate=row['换手率']    
  )

"""
AList
"""
class AListResponse(ResponseModel):
  result: list[AListModel]

@router.post('/alist', response_model=AListResponse, response_model_exclude_none=True)
async def alist():
  df = stock.get_a_list()
  ret: list[AListModel] = []
  print(datetime.now())
  for _, row in df.iterrows():
    ret.append({
      'code': row['code'],
      'name': row['name']
    })
  print(datetime.now())
  return AListResponse(result=ret)

"""
History
"""
class HistoryRequest(RequestModel):
  code: str
  period: str | None = Field(default='daily', description='daily/weekly/monthly')
  start: str | None = None
  end: str | None = None
  adjust: str | None = Field(default='qfq', description='qfq/hfq')

class HistoryResponse(ResponseModel):
  result: list[HistoryDataModel]

@router.post('/history', response_model=HistoryResponse, response_model_exclude_none=True)
async def history(body: HistoryRequest=Body()):
  try:
    ret = []
    df = stock.get_history(body.code, body.start, body.end, None, body.period, body.adjust)
    for _, row in df.iterrows():
      ret.append(history_data2model(row))
    return HistoryResponse(result=ret)
  except Exception as e:
    raise AppException(e)
