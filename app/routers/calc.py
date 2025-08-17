
from typing import List, Optional
from fastapi import APIRouter, Depends
from app.database import calc as db
from app.routers.common import DEFAULT_UID, RequestModel, ResponseModel, verify_token

router: APIRouter = APIRouter(prefix="/calc", tags=["Calc"], dependencies=[Depends(verify_token)])

class AlgorithmItemCreateRequest(RequestModel):
  name: str
  category: int
  type: int
  list_type: int
  data_period: int
  report_period: int
  remarks: Optional[str] = None

class AlgorithmItemCreateResponse(ResponseModel):
  result: int

@router.post('/create', response_model=AlgorithmItemCreateResponse)
async def create_algorithm_item(request: AlgorithmItemCreateRequest):
  result = db.insert_algorithm_item(uid=DEFAULT_UID, name=request.name, category=request.category, type=request.type, list_type=request.list_type, data_period=request.data_period, report_period=request.report_period, remarks=request.remarks)
  return AlgorithmItemCreateResponse(result=result)

class AlgorithmItemsRequest(RequestModel):
  pass

class AlgorithmItemsResponse(ResponseModel):
   result: list[db.CalcAlgorithmItemModel] = []

@router.post("/list", response_model=AlgorithmItemsResponse)
async def list_algorithm_items(request: AlgorithmItemsRequest):
  result = db.select_algorithm_items(uid=DEFAULT_UID)
  return AlgorithmItemsResponse(result=result)

class AlgorithmItemDeleteRequest(RequestModel):
  id: int

class AlgorithmItemDeleteResponse(ResponseModel):
  result: int

@router.post("/remove", response_model=AlgorithmItemDeleteResponse)
async def delete_algorithm_item(request: AlgorithmItemDeleteRequest):
  db.delete_algorithm_item(uid=DEFAULT_UID, id=request.id)
  return AlgorithmItemDeleteResponse(result=0)

class StockListCreateRequest(RequestModel):
  cid: int
  items: List[db.CalcAlgorithmItemStockListModel]

class StockListCreateResponse(ResponseModel):
  result: int

@router.post('/stock_list_create', response_model=StockListCreateResponse)
async def create_stock_list(request: StockListCreateRequest):
  db.delete_algorithm_item_stock_list(cid=request.cid)
  db.insert_algorithm_item_stock_list(cid=request.cid, items=request.items)
  return StockListCreateResponse(result=0)

class StockListRequest(RequestModel):
  cid: int

class StockListResponse(ResponseModel):
   result: list[db.CalcAlgorithmItemStockListModel] = []

@router.post("/stock_list", response_model=StockListResponse)
async def list_stock_list(request: StockListRequest):
  result = db.select_algorithm_item_stock_list(cid=request.cid)
  return StockListResponse(result=result)

class StockListDeleteRequest(RequestModel):
  cid: int
  id: Optional[int] = None

class StockListDeleteResponse(ResponseModel):
  result: int

@router.post("/stock_list_remove", response_model=StockListDeleteResponse)
async def delete_stock_list(request: StockListDeleteRequest):
  db.delete_algorithm_item_stock_list(cid=request.cid, id=request.id)
  return StockListDeleteResponse(result=0)

class ArgumentsCreateRequest(RequestModel):
  cid: int
  items: List[db.CalcAlgorithmItemArgumentsModel]

class ArgumentsCreateResponse(ResponseModel):
  result: int

@router.post('/arguments_create', response_model=ArgumentsCreateResponse)
async def create_arguments(request: ArgumentsCreateRequest):
  db.delete_algorithm_item_arguments(cid=request.cid)
  db.insert_algorithm_item_arguments(uid=DEFAULT_UID, cid=request.cid, items=request.items)
  return ArgumentsCreateResponse(result=0)

class ArgumentsRequest(RequestModel):
  cid: int

class ArgumentsResponse(ResponseModel):
   result: list[db.CalcAlgorithmItemArgumentsModel] = []

@router.post("/arguments", response_model=ArgumentsResponse)
async def list_arguments(request: ArgumentsRequest):
  result = db.select_algorithm_item_arguments(cid=request.cid)
  return ArgumentsResponse(result=result)

class ArgumentsDeleteRequest(RequestModel):
  cid: int
  id: Optional[int] = None

class ArgumentsDeleteResponse(ResponseModel):
  result: int

@router.post("/arguments_remove", response_model=ArgumentsDeleteResponse)
async def delete_arguments(request: ArgumentsDeleteRequest):
  db.delete_algorithm_item_arguments(cid=request.cid, id=request.id)
  return ArgumentsDeleteResponse(result=0)
