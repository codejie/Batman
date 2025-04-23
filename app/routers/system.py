from typing import Optional
import zipfile
from datetime import datetime
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from app.database import dbEngine, funds, holding
from app.routers.common import RequestModel, verify_token

router: APIRouter = APIRouter(prefix="/system", tags=["System"], dependencies=[Depends(verify_token)])

Export_Import_Tables = [
  holding.HoldingTable,
  holding.HoldingOperationTable,
  funds.FundsTable,
  funds.FundsOperationTable
]

Export_Import_Path = './app/db'

def zip(file_name: str, files: list[str]) -> str:
  with zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED) as zip:
    for file in files:
      zip.write(file)
  return file_name

# init db, stock info etc.

"""
data export
"""
class ExportRequest(RequestModel):
  flag: Optional[int] = None

@router.post('/db/export')
async def db_export(request: ExportRequest = None):
  files = [f'{Export_Import_Path}/{item.__tablename__}.json' for item in Export_Import_Tables]
  for table in Export_Import_Tables:
    # file = f'./app/db/{files[tables.index(table)]}'
    dbEngine.export_json(table, files[Export_Import_Tables.index(table)])

  output = f'export_{datetime.now().strftime("%Y-%m-%d")}.zip'
  zip(f'{Export_Import_Path}/{output}', files)

  return FileResponse(
    path=f'{Export_Import_Path}/{output}',
    filename=output,
    media_type='application/zip'
  )

class ImportResponse(RequestModel):
  result: int

@router.post('/db/import', response_model=ImportResponse)
async def db_import(request: ExportRequest = None, file: UploadFile = File(...)):
  zip_file = f'{Export_Import_Path}/{file.filename}'
  with open(zip_file, 'wb') as f:
    f.write(file.file.read())

  with zipfile.ZipFile(zip_file, 'r') as zip:
    zip.extractall(Export_Import_Path)

  files = [f'{Export_Import_Path}/{item.__tablename__}.json' for item in Export_Import_Tables]
  for table in Export_Import_Tables:
    dbEngine.import_json(table, files[Export_Import_Tables.index(table)])

  return ImportResponse(result=0)
