from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, select, delete
from app.database import TableBase, dbEngine
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CalcAlgorithmItemsTable(TableBase):
  __tablename__ = 'calc_algorithm_items'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  uid = Column(Integer, nullable=False, default=99)
  name = Column(String, nullable=False)
  remarks = Column(String)
  category = Column(Integer, nullable=False)
  type = Column(Integer, nullable=False)
  list_type = Column(Integer, nullable=False, default=2)  # 0: holding, 1: customized, 2: holding + customized, 3custom, 4: all
  data_period = Column(Integer, nullable=False, default=1)  # 0: 3months, 1: 6months, 2: 1year, 3: 2years
  report_period = Column(String, nullable=False, default='1') # 0: today, 1: 3days, 2: 1week, 3: 1monthly, 4: all
  created = Column(DateTime, default=func.now())

class CalcAlgorithmItemModel(BaseModel):
  id: Optional[int]
  uid: int
  name: str
  remarks: str | None = None
  category: int
  type: int
  list_type: int
  data_period: int
  report_period: str
  created: datetime

class CalcAlgorithmItemStockListTable(TableBase):
  __tablename__ = 'calc_algorithm_item_stock_list'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  cid = Column(Integer, ForeignKey('calc_algorithm_items.id'), nullable=False)
  type = Column(Integer, nullable=False)  # 2: stock, 1: index
  code = Column(String, nullable=False)

class CalcAlgorithmItemStockListModel(BaseModel):
  id: int | None = None
  cid: int
  type: int
  code: str

class CalcAlgorithmItemArgumentsTable(TableBase):
  __tablename__ = 'calc_algorithm_item_arguments'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  cid = Column(Integer, ForeignKey('calc_algorithm_items.id'), nullable=False)
  category = Column(Integer, nullable=False)
  type = Column(Integer, nullable=False)
  arguments = Column(String, nullable=False)  # JSON string
  flag = Column(Integer, default=0)

class CalcAlgorithmItemArgumentsModel(BaseModel):
  id: int | None = None
  cid: int
  category: int
  type: int
  arguments: dict
  flag: int

  def model_dump(self, *args, **kwargs) -> dict:
    data = super().model_dump(*args, **kwargs)
    # Convert arguments to JSON string
    if isinstance(data["arguments"], dict):
      data["arguments"] = str(data["arguments"])
    return data

def insert_algorithm_item(uid: int, name: str, category: int, type: int, list_type: int = 2, data_period: int = 1, report_period: str = '1', remarks: str | None = None) -> int:
  item = CalcAlgorithmItemsTable(uid=uid, name=name, category=category, type=type, list_type=list_type, data_period=data_period, report_period=report_period, remarks=remarks)
  return dbEngine.insert_instance(item)

def insert_algorithm_item_stock_list(items: List[CalcAlgorithmItemStockListModel]) -> None:
  if not items:
    return
  items = [item.model_dump() for item in items]
  dbEngine.bulk_insert_data(CalcAlgorithmItemStockListTable, items)

def insert_algorithm_item_arguments(items: List[CalcAlgorithmItemArgumentsModel]) -> None:
  if not items:
    return
  items = [item.model_dump() for item in items]
  dbEngine.bulk_insert_data(CalcAlgorithmItemArgumentsTable, items)

def select_algorithm_items(uid: int) -> List[CalcAlgorithmItemModel]:
  stmt = select(CalcAlgorithmItemsTable).where(CalcAlgorithmItemsTable.uid == uid)
  results = dbEngine.select_scalars(stmt)
  return results

def select_algorithm_item_stock_list(cid: int) -> List[CalcAlgorithmItemStockListModel]:
  stmt = select(CalcAlgorithmItemStockListTable).where(CalcAlgorithmItemStockListTable.cid == cid)
  results = dbEngine.select_scalars(stmt)
  return results

def select_algorithm_item_arguments(cid: int) -> List[CalcAlgorithmItemArgumentsModel]:
  stmt = select(CalcAlgorithmItemArgumentsTable).where(CalcAlgorithmItemArgumentsTable.cid == cid)
  result = dbEngine.select_scalars(stmt)
  for item in result:
    if isinstance(item.arguments, str):
      item.arguments = eval(item.arguments)
  return result

def delete_algorithm_item(uid: int, id: int) -> None:
  dbEngine.execute_stmt(delete(CalcAlgorithmItemStockListTable).where(CalcAlgorithmItemStockListTable.cid == id))
  dbEngine.execute_stmt(delete(CalcAlgorithmItemArgumentsTable).where(CalcAlgorithmItemArgumentsTable.cid == id))
  dbEngine.execute_stmt(delete(CalcAlgorithmItemsTable).where(CalcAlgorithmItemsTable.id == id).where(CalcAlgorithmItemsTable.uid == uid))

def delete_algorithm_item_stock_list(cid: int, id: int | None= None) -> None:
  stmt = delete(CalcAlgorithmItemStockListTable).where(CalcAlgorithmItemStockListTable.cid == cid)
  if id is not None:
    stmt = stmt.where(CalcAlgorithmItemStockListTable.id == id)
  dbEngine.execute_stmt(stmt)

def delete_algorithm_item_arguments(cid: int, id: int | None = None) -> None:
  stmt = delete(CalcAlgorithmItemArgumentsTable).where(CalcAlgorithmItemArgumentsTable.cid == cid)
  if id is not None:
    stmt = stmt.where(CalcAlgorithmItemArgumentsTable.id == id)
  dbEngine.execute_stmt(stmt)