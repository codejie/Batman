from pandas import Series
from pydantic import Field
from app.database import index
from app.exception import AppException
from app.routers.definition import BaseModel, RequestModel, ResponseModel, APIRouter, Depends, Body, verify_token

router: APIRouter = APIRouter(prefix='/data/index', tags=['data', 'index'], dependencies=[Depends(verify_token)])

"""
Data Model
"""
class AListModel(BaseModel):
  code: str
  name: str
  market: str

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
  df = index.get_a_list()
  ret: list[AListModel] = []
  for _, row in df.iterrows():
    ret.append({
      'code': row['code'],
      'name': row['name'],
      'market': row['market']
    })
  return AListResponse(result=ret)

"""
Info
"""
class InfoRequest(RequestModel):
  code: str

class InfoResponse(ResponseModel):
  result: AListModel | None

@router.post('/info', response_model=InfoResponse, response_model_exclude_none=True)
async def info(body: InfoRequest=Body()):
  df = index.get_info(body.code)
  return InfoResponse(result=AListModel(code=df['code'][0], name=df['name'][0], market=df['market'][0]) if len(df) > 0 else None)

"""
History
"""
class HistoryRequest(RequestModel):
  code: str
  period: str | None = Field(default='daily', description='daily/weekly/monthly')
  start: str | None = None
  end: str | None = None

class HistoryResponse(ResponseModel):
  result: list[HistoryDataModel]

@router.post('/history', response_model=HistoryResponse, response_model_exclude_none=True)
async def history(body: HistoryRequest=Body()):
  try:
    ret = []
    df = index.get_history(body.code, body.start, body.end, None, body.period)
    for _, row in df.iterrows():
      ret.append(history_data2model(row))
    return HistoryResponse(result=ret)
  except Exception as e:
    raise AppException(e)