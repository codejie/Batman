from typing import Optional
from fastapi import APIRouter, Depends
from app.database import data as Data
from app.database.data.define import ADJUST_QFQ, PERIOD_DAILY, TYPE_STOCK, HistoryData
from app.routers.common import RequestModel, ResponseModel, verify_token, verify_system_token

router: APIRouter = APIRouter(prefix="/data", tags=["Data"], dependencies=[Depends(verify_token)])

"""
Name
"""
class GetNameRequest(RequestModel):
  type: int
  code: str

class GetNameResponse(ResponseModel):
  result: str

@router.post("/get_name", response_model=GetNameResponse)
async def get_name_api(request: GetNameRequest):
  result = Data.get_name(type=request.type, code=request.code)
  return GetNameResponse(result=result)

"""
download list
"""
class DownloadListRequest(RequestModel):
  type: int

class DownloadListResponse(ResponseModel):
  pass

@router.post("/download_list", response_model=DownloadListResponse, dependencies=[Depends(verify_system_token)])
async def download_list_api(request: DownloadListRequest):
  Data.download_list(type=request.type)
  return DownloadListResponse()

"""
download history data
"""
class DownloadHistoryRequest(RequestModel):
  type: int
  code: str
  start: str
  end: str
  period: str = 'daily'
  adjust: Optional[str] = None

class DownloadHistoryResponse(ResponseModel):
  result: int

@router.post("/download_history", response_model=DownloadHistoryResponse, dependencies=[Depends(verify_system_token)])
async def download_history_api(request: DownloadHistoryRequest):
  result = Data.download_history_data(
    type=request.type,
    code=request.code,
    start=request.start,
    end=request.end,
    period=request.period,
    adjust=request.adjust
  )
  return DownloadHistoryResponse(result=result)

"""
get history data
"""
class GetHistoryDataRequest(RequestModel):
  type: int
  code: str
  start: Optional[str] = None
  end: Optional[str] = None
  period: Optional[str] = 'daily'
  adjust: Optional[str] = None

class GetHistoryDataResponse(ResponseModel):
  result: list[HistoryData] = []

@router.post("/get_history_data", response_model=GetHistoryDataResponse)
async def get_history_data_api(request: GetHistoryDataRequest):
  if request.period is None:
    request.period = PERIOD_DAILY
  if request.type == TYPE_STOCK and request.adjust is None:
    request.adjust = ADJUST_QFQ
    
  result = Data.get_history_data(
    type=request.type,
    code=request.code,
    start=request.start,
    end=request.end,
    period=request.period,
    adjust=request.adjust
  )
  return GetHistoryDataResponse(result=result)

class GetLatestHistoryDataRequest(RequestModel):
  type: int
  code: str
  period: str = 'daily'
  adjust: str = 'qfq'

class GetLatestHistoryDataResponse(ResponseModel):
  result: Optional[HistoryData] = None

@router.post("/get_latest_history_data", response_model=GetLatestHistoryDataResponse)
async def get_latest_history_data_api(request: GetLatestHistoryDataRequest):
  result = Data.get_latest_history_data(
    type=request.type,
    code=request.code,
    period=request.period,
    adjust=request.adjust
  )
  return GetLatestHistoryDataResponse(result=result)

class RemoveHistoryDataRequest(RequestModel):
  pass

class RemoveHistoryDataResponse(ResponseModel):
  result: int = 0

@router.post("/remove_history_data", response_model=RemoveHistoryDataResponse, dependencies=[Depends(verify_system_token)])
async def remove_history_data_api(request: RemoveHistoryDataRequest):
  result = Data.remove_all_history_data()
  return RemoveHistoryDataResponse(result=result)