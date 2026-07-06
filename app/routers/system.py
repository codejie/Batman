import json
import os
from typing import Optional
import zipfile
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.database import dbEngine, funds, holding, customized
from app.database.data import data_source as DataSource
from app.routers.common import RequestModel, ResponseModel, verify_token

router: APIRouter = APIRouter(prefix="/system", tags=["System"]) #, dependencies=[Depends(verify_token)])

Export_Import_Tables = [
  holding.HoldingTable,
  holding.HoldingOperationTable,
  funds.FundsTable,
  funds.FundsOperationTable,
  customized.CustomizedRecordTable
]

Export_Import_Root = './app/tmp'
Export_Path = f'{Export_Import_Root}/export'
Import_Path = f'{Export_Import_Root}/import'
System_Data_Root = './app/db'
Trade_Calendar_Path = f'{System_Data_Root}/trade_calendar'

DEFAULT_NON_TRADE_MONTH_DAYS: set[str] = {
  '01-01',
  '05-01', '05-02', '05-03',
  '10-01', '10-02', '10-03', '10-04', '10-05'
}

def zip(file_name: str, files: list[str]) -> str:
  with zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED) as zip:
    for file in files:
      name = os.path.basename(file)
      zip.write(filename=file, arcname=name)
  return file_name

def trade_calendar_file(year: int) -> str:
  return f'{Trade_Calendar_Path}/{year}.json'

def year_dates(year: int) -> list[str]:
  current = date(year, 1, 1)
  end = date(year + 1, 1, 1)
  results: list[str] = []
  while current < end:
    results.append(current.isoformat())
    current += timedelta(days=1)
  return results

def make_default_trade_calendar(year: int) -> dict:
  trade_days: list[str] = []
  non_trade_days: list[str] = []

  for day in year_dates(year):
    current = date.fromisoformat(day)
    if current.weekday() >= 5 or day[5:] in DEFAULT_NON_TRADE_MONTH_DAYS:
      non_trade_days.append(day)
    else:
      trade_days.append(day)

  return {
    'year': year,
    'trade_days': trade_days,
    'non_trade_days': non_trade_days,
    'source': 'default'
  }

def read_trade_calendar(year: int) -> dict:
  file_name = trade_calendar_file(year)
  if os.path.exists(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
      data = json.load(f)
      data['source'] = 'saved'
      return data
  return make_default_trade_calendar(year)

def normalize_trade_calendar(year: int, trade_days: list[str], non_trade_days: list[str]) -> dict:
  valid_days = set(year_dates(year))
  trade_day_set = {day for day in trade_days if day in valid_days}
  non_trade_day_set = {day for day in non_trade_days if day in valid_days}

  if not trade_day_set and not non_trade_day_set:
    return make_default_trade_calendar(year)

  trade_day_set -= non_trade_day_set
  missing_days = valid_days - trade_day_set - non_trade_day_set
  for day in missing_days:
    current = date.fromisoformat(day)
    if current.weekday() >= 5:
      non_trade_day_set.add(day)
    else:
      trade_day_set.add(day)

  return {
    'year': year,
    'trade_days': sorted(trade_day_set),
    'non_trade_days': sorted(non_trade_day_set),
    'source': 'saved'
  }

# init db, stock info etc.

"""
data export
"""
class ExportRequest(RequestModel):
  flag: Optional[int] = None

class ExportResult(BaseModel):
  path: str
  filename: str
  media_type: str

class ExportResponse(FileResponse):
  def __init__(self, code, result, path, status_code = 200, headers = None, media_type = None, background = None, filename = None, stat_result = None, method = None, content_disposition_type = "attachment"):
    super().__init__(path, status_code, headers, media_type, background, filename, stat_result, method, content_disposition_type)
    self.code = code
    self.result = result

@router.post('/db/export')
async def db_export(request: ExportRequest = None):
  os.makedirs(Export_Path, exist_ok=True)
  files = [f'{Export_Path}/{item.__tablename__}.json' for item in Export_Import_Tables]
  for table in Export_Import_Tables:
    # file = f'./app/db/{files[tables.index(table)]}'
    dbEngine.export_json(table, files[Export_Import_Tables.index(table)])

  output = f'export_{datetime.now().strftime("%Y-%m-%d")}.zip'
  zip(f'{Export_Path}/{output}', files)

  # return ExportResponse(
  #   code=0,
  #   result='',
  #   path=f'{Export_Import_Path}/{output}',
  #   filename=output,
  #   media_type='application/zip'
  # )

  return FileResponse(
    path=f'{Export_Path}/{output}',
    filename=output,
    media_type='application/zip'
  )

class ImportRequest(RequestModel):
  pass

class ImportResponse(ResponseModel):
  result: int

@router.post('/db/import', response_model=ImportResponse)
async def db_import(request: ExportRequest = None, file: UploadFile = File(...)):
  os.makedirs(Import_Path, exist_ok=True)
  zip_file = f'{Import_Path}/{file.filename}'
  with open(zip_file, 'wb') as f:
    f.write(file.file.read())

  with zipfile.ZipFile(zip_file, 'r') as zip:
    zip.extractall(Import_Path)

  files = [f'{Import_Path}/{item.__tablename__}.json' for item in Export_Import_Tables]
  for table in Export_Import_Tables:
    dbEngine.import_json(table, files[Export_Import_Tables.index(table)])

  return ImportResponse(result=0)

class TradeCalendarGetRequest(RequestModel):
  year: int

class TradeCalendarData(BaseModel):
  year: int
  trade_days: list[str]
  non_trade_days: list[str]
  source: str = 'default'

class TradeCalendarGetResponse(ResponseModel):
  result: TradeCalendarData

@router.post('/trade_calendar/get', response_model=TradeCalendarGetResponse)
async def trade_calendar_get(request: TradeCalendarGetRequest):
  result = read_trade_calendar(request.year)
  return TradeCalendarGetResponse(result=TradeCalendarData(**result))

class TradeCalendarSaveRequest(RequestModel):
  year: int
  trade_days: list[str]
  non_trade_days: list[str]

class TradeCalendarSaveResponse(ResponseModel):
  result: TradeCalendarData

@router.post('/trade_calendar/save', response_model=TradeCalendarSaveResponse)
async def trade_calendar_save(request: TradeCalendarSaveRequest):
  os.makedirs(Trade_Calendar_Path, exist_ok=True)
  result = normalize_trade_calendar(request.year, request.trade_days, request.non_trade_days)
  with open(trade_calendar_file(request.year), 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
  return TradeCalendarSaveResponse(result=TradeCalendarData(**result))

class DataConfigGetRequest(RequestModel):
  pass

class DataConfigData(BaseModel):
  market_data_source: str

class DataConfigGetResponse(ResponseModel):
  result: DataConfigData

@router.post('/data_config/get', response_model=DataConfigGetResponse)
async def data_config_get(request: DataConfigGetRequest):
  result = DataSource.read_data_config()
  return DataConfigGetResponse(result=DataConfigData(**result))

class DataConfigSaveRequest(RequestModel):
  market_data_source: str

class DataConfigSaveResponse(ResponseModel):
  result: DataConfigData

@router.post('/data_config/save', response_model=DataConfigSaveResponse)
async def data_config_save(request: DataConfigSaveRequest):
  result = DataSource.save_data_config(request.market_data_source)
  return DataConfigSaveResponse(result=DataConfigData(**result))
