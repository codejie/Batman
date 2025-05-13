import os
from typing import Optional
import zipfile
from datetime import datetime
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.database import dbEngine, funds, holding, customized
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

def zip(file_name: str, files: list[str]) -> str:
  with zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED) as zip:
    for file in files:
      name = os.path.basename(file)
      zip.write(filename=file, arcname=name)
  return file_name

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
