from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, select, delete, and_, update
from app.database import TableBase, dbEngine
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.database.data.define import InfoTable

class CalcAlgorithmItemsTable(TableBase):
  __tablename__ = 'calc_algorithm_items'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  uid = Column(Integer, nullable=False, default=99)
  name = Column(String, nullable=False)
  remarks = Column(String)
  list_type = Column(Integer, nullable=False, default=4)  # 0: holding, 1: customized, 2:custom, 3: all, 4: holding & watchlist
  data_period = Column(Integer, nullable=False, default=1)  # 0: 3months, 1: 6months, 2: 1year, 3: 2years
  report_period = Column(Integer, nullable=False, default=1) # 0: today, 1: 3days, 2: 1week, 3: 1monthly, 4: all
  show_opt = Column(Integer, nullable=False, default=0) # 0: hide, 1: show
  created = Column(DateTime, default=func.now())

class CalcAlgorithmItemModel(BaseModel):
  id: Optional[int]
  uid: int
  name: str
  remarks: str | None = None
  list_type: int
  data_period: int
  report_period: int
  show_opt: int
  created: datetime

class CalcAlgorithmItemStockListTable(TableBase):
  __tablename__ = 'calc_algorithm_item_stock_list'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  cid = Column(Integer, ForeignKey('calc_algorithm_items.id'), nullable=False)
  type = Column(Integer, nullable=False)  # 2: stock, 1: index
  code = Column(String, nullable=False)

class CalcAlgorithmItemStockListModel(BaseModel):
  id: int | None = None
  cid: int | None = None
  type: int
  code: str
  name: str | None = None

  def model_dump(self, *args, **kwargs):
    data = super().model_dump(*args, **kwargs)
    data.pop('name', None)
    return data

class CalcAlgorithmItemArgumentsTable(TableBase):
  __tablename__ = 'calc_algorithm_item_arguments'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  cid = Column(Integer, ForeignKey('calc_algorithm_items.id'), nullable=False) # calc id
  category = Column(String, nullable=False) # category
  type = Column(String, nullable=False) # id
  arguments = Column(String, nullable=False)  # JSON string
  flag = Column(Integer, nullable=True, default=0)

class CalcAlgorithmItemArgumentsModel(BaseModel):
  id: int | None = None
  cid: int
  category: str
  type: str
  arguments: str
  flag: int | None = 0

  # def model_dump(self, *args, **kwargs) -> dict:
  #   data = super().model_dump(*args, **kwargs)
  #   # Convert arguments to JSON string
  #   if isinstance(data["arguments"], dict):
  #     data["arguments"] = str(data["arguments"])
  #   return data




def insert_algorithm_item(uid: int, name: str, list_type: int = 2, data_period: int = 1, report_period: int = 1, show_opt: int = 0, remarks: str | None = None) -> int:
  item = CalcAlgorithmItemsTable(uid=uid, name=name, list_type=list_type, data_period=data_period, report_period=report_period, show_opt=show_opt, remarks=remarks)
  return dbEngine.insert_instance(item)

def update_algorithm_item(uid: int, id: int, name: str, list_type: int, data_period: int, report_period: int, show_opt: int, remarks: str | None = None) -> None:
    stmt = update(CalcAlgorithmItemsTable).where(
        and_(
            CalcAlgorithmItemsTable.id == id,
            CalcAlgorithmItemsTable.uid == uid
        )
    ).values(
        name=name,
        remarks=remarks,
        list_type=list_type,
        data_period=data_period,
        report_period=report_period,
        show_opt=show_opt
    )
    dbEngine.execute_stmt(stmt)

def insert_algorithm_item_stock_list(cid: int, items: List[CalcAlgorithmItemStockListModel]) -> None:
  if not items or len(items) == 0:
    return
  for item in items:
    item.cid = cid
  items = [item.model_dump() for item in items]
  dbEngine.bulk_insert_data(CalcAlgorithmItemStockListTable, items)

def insert_algorithm_item_arguments(uid: int, cid: int, items: List[CalcAlgorithmItemArgumentsModel]) -> None:
  if not items:
    return
  items = [item.model_dump() for item in items]
  dbEngine.bulk_insert_data(CalcAlgorithmItemArgumentsTable, items)

def select_algorithm_items(uid: int) -> List[CalcAlgorithmItemModel]:
  stmt = select(CalcAlgorithmItemsTable).where(CalcAlgorithmItemsTable.uid == uid)
  results = dbEngine.select_stmt(stmt)
  results = [CalcAlgorithmItemModel(
    id=item[0].id,
    uid=item[0].uid,
    name=item[0].name,
    remarks=item[0].remarks,
    list_type=item[0].list_type,
    data_period=item[0].data_period,
    report_period=item[0].report_period,
    show_opt=item[0].show_opt,
    created=item[0].created
  ) for item in results]
  return results

def select_algorithm_item(uid: int, id: int) -> Optional[CalcAlgorithmItemModel]:
  stmt = select(CalcAlgorithmItemsTable).where(
    and_(
      CalcAlgorithmItemsTable.uid == uid,
      CalcAlgorithmItemsTable.id == id
    )
  )
  results = dbEngine.select_stmt(stmt)
  if results:
    item = results[0][0]
    return CalcAlgorithmItemModel(
      id=item.id,
      uid=item.uid,
      name=item.name,
      remarks=item.remarks,
      list_type=item.list_type,
      data_period=item.data_period,
      report_period=item.report_period,
      show_opt=item.show_opt,
      created=item.created
    )
  return None

def select_algorithm_item_stock_list(cid: int) -> List[CalcAlgorithmItemStockListModel]:
  stmt = select(CalcAlgorithmItemStockListTable, InfoTable.name).join(
      InfoTable, and_(
          CalcAlgorithmItemStockListTable.code == InfoTable.code,
          CalcAlgorithmItemStockListTable.type == InfoTable.type
      )
  ).where(CalcAlgorithmItemStockListTable.cid == cid)
  results = dbEngine.select_stmt(stmt)
  results = [CalcAlgorithmItemStockListModel(
    id=item[0].id,
    cid=item[0].cid,
    type=item[0].type,
    code=item[0].code,
    name=item[1]
  ) for item in results]
  return results

def select_algorithm_item_arguments(cid: int) -> List[CalcAlgorithmItemArgumentsModel]:
  stmt = select(CalcAlgorithmItemArgumentsTable).where(CalcAlgorithmItemArgumentsTable.cid == cid)
  result = dbEngine.select_stmt(stmt)
  # for item in result:
  #   if isinstance(item.arguments, str):
  #     item.arguments = eval(item.arguments)
  results = [CalcAlgorithmItemArgumentsModel(
    id=item[0].id,
    cid=item[0].cid,
    category=item[0].category,
    type=item[0].type,
    arguments=item[0].arguments,
    flag=item[0].flag
  ) for item in result]
  return results

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
