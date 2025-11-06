import datetime
from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Index, Integer, PrimaryKeyConstraint, String, DateTime, and_, case, delete, select, update
from sqlalchemy.sql import func
from app.database import dbEngine, TableBase
from app.database.data import define as Data
from app.logger import logger

HOLDING_FLAG_ACTIVE: int = 1
HOLDING_FLAG_REMOVED: int = 2
HOLDING_FLAG_SOLDOUT: int = 3
OPERATION_ACTION_BUY: int = 1
OPERATION_ACTION_SELL: int = 2
OPERATION_ACTION_SOLDOUT: int = 3
OPERATION_ACTION_INTEREST: int = 4

class HoldingTable(TableBase):
  __tablename__ = 'user_holding_table'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
  uid = Column(Integer, nullable=False, default=99)
  type = Column(Integer, nullable=False)
  code = Column(String, nullable=False)
  flag = Column(Integer, nullable=False, default=HOLDING_FLAG_ACTIVE)
  created = Column(DateTime(timezone=True), server_default=func.now())
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

  __table_args__ = (
    Index('idx_user_holding_type_code', 'type', 'code'),
  )

class HoldingOperationTable(TableBase):
  __tablename__ = 'user_holding_operation_table'

  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  holding = Column(Integer, ForeignKey(HoldingTable.id), nullable=False)
  action = Column(Integer, nullable=False)
  quantity = Column(Integer, nullable=False) # 买入为正，卖出为负
  price = Column(Float, nullable=False) # 买入/卖出价
  expense = Column(Float, nullable=False) # 买入为负，卖出为正
  comment = Column(String, nullable=True)
  created = Column(DateTime(timezone=True), server_default=func.now())

class UserHoldingRecord(BaseModel):
  id: int
  type: int
  code: str
  name: str
  flag: int
  created: datetime.datetime
  updated: datetime.datetime
  quantity: int
  expense: float

def insert_holding(uid: int, type: int, code: str, flag: int = HOLDING_FLAG_ACTIVE) -> int:
  return dbEngine.insert_instance(HoldingTable(uid=uid, type=type, code=code, flag=flag))

def insert_operation(id: int, action: int, quantity: int, price: float, expense: float, comment: str = None, created: datetime.datetime = None) -> int:
  logger.debug(f"insert_operation called with: id={id}, action={action}, quantity={quantity}, price={price}, expense={expense}, comment={comment}, created={created}")

  if action == OPERATION_ACTION_BUY:
    logger.debug(f"Action BUY: quantity={quantity}, expense={-expense}")
    return dbEngine.insert_instance(HoldingOperationTable(holding=id, action=action, quantity=quantity, price=price, expense=-expense, comment=comment, created=created))
  
  if action == OPERATION_ACTION_INTEREST:
    logger.debug(f"Action INTEREST: quantity=0, expense={expense}")
    return dbEngine.insert_instance(HoldingOperationTable(holding=id, action=action, quantity=0, price=price, expense=expense, comment=comment, created=created))

  if action == OPERATION_ACTION_SELL:
    logger.debug(f"Action SELL: Initial quantity={quantity}, price={price}, expense={expense}")
    current_quantity, current_expense = get_holding_summary(id)
    logger.debug(f"SELL: current_quantity={current_quantity}, current_expense={current_expense}")
    
    # 1. 首先，总是插入 SELL 操作记录
    sell_op_id = dbEngine.insert_instance(HoldingOperationTable(
        holding=id, action=OPERATION_ACTION_SELL, quantity=-quantity, price=price, expense=expense, comment=comment, created=created
    ))
    logger.debug(f"SELL operation inserted with id={sell_op_id}")

    # 2. 如果是清仓，则执行附加操作
    if quantity == current_quantity:
      logger.debug(f"SELL: This is a full sellout. quantity={quantity} == current_quantity={current_quantity}")
      # 计算利润并插入 SOLDOUT 摘要记录
      # 根据用户定义，清仓盈亏为当前持有费用与卖出操作费用的和 (即所有操作expense的累加)
      profit = expense + current_expense
      logger.debug(f"SELL (SOLDOUT): Calculated profit={profit}")
      dbEngine.insert_instance(HoldingOperationTable(
          holding=id, action=OPERATION_ACTION_SOLDOUT, quantity=quantity, price=price, expense=profit, comment="清仓", created=created
      ))
      logger.debug(f"SOLDOUT operation inserted with profit={profit}")

      # 将持股标志更新为 SOLDOUT
      holding_records = dbEngine.select_stmt(select(HoldingTable).where(HoldingTable.id == id))
      if holding_records:
          holding_record = holding_records[0]
          logger.debug(f"SELL (SOLDOUT): Updating holding flag for holding_id={id} to HOLDING_FLAG_SOLDOUT. uid={holding_record[0].uid}")
          update_holding_flag(holding_record[0].uid, id, HOLDING_FLAG_SOLDOUT)
          logger.debug(f"SELL (SOLDOUT): Holding flag updated.")
          
    return sell_op_id
  
  # 对于任何其他操作类型，直接插入
  logger.debug(f"Action OTHER: quantity={quantity}, expense={expense}")
  return dbEngine.insert_instance(HoldingOperationTable(holding=id, action=action, quantity=quantity, price=price, expense=expense, comment=comment, created=created))

def select_holding(uid: int, type: int = None, code: str = None, flag: int = None) -> list[HoldingTable]:
  stmt = select(HoldingTable).where(HoldingTable.uid == uid)
  if type:
    stmt = stmt.where(HoldingTable.type == type)
  if code: 
    stmt = stmt.where(HoldingTable.code == code)
  if flag:
    stmt = stmt.where(HoldingTable.flag == flag)
  return dbEngine.select_stmt(stmt)

def select_operation(uid: int, holding: int = None) -> list[HoldingOperationTable]:
  stmt = select(HoldingOperationTable).order_by(HoldingOperationTable.created.asc())
  if holding:
    stmt = stmt.where(HoldingOperationTable.holding == holding)
  return dbEngine.select_stmt(stmt)

def update_holding_flag(uid: int, id: int, flag: int) -> int:
  return dbEngine.update_stmt(update(HoldingTable).where(HoldingTable.id == id and HoldingTable.uid == uid).values({
    'flag': flag, 'updated': func.now()
  }))

def delete_operation(uid: int, id: int) -> int:
  return dbEngine.delete_stmt(delete(HoldingOperationTable).where(HoldingOperationTable.id == id))
"""
Combination API
"""
def create(uid: int, type: int, code: str, action: int, quantity: int, price: float, expense: float, comment: str = None) -> int:
  records = dbEngine.select_stmt(select(HoldingTable)
                                 .where(HoldingTable.uid == uid)
                                 .where(HoldingTable.type == type)
                                 .where(HoldingTable.code == code))
  id = -1
  if len(records) == 0:
    id = dbEngine.insert_instance(HoldingTable(uid=uid, type=type, code=code))
  else:
    id = records[0].id
    if records[0].flag == HOLDING_FLAG_REMOVED:
      dbEngine.update_stmt(update(HoldingTable).where(HoldingTable.id == id).values([
        {'flag': HOLDING_FLAG_ACTIVE, 'updated': func.now()}
      ]))
  dbEngine.insert_instance(HoldingOperationTable(holding=id, action=action, quantity=quantity, price=price, expense=expense, comment=comment))
  return id

def records(uid: int, id: int = None, type: int = None, code: str = None, flag: int = None) -> list[UserHoldingRecord]:
  # stmt = select(HoldingTable,
  #               Data.InfoTable.name.label('name'),
  #               func.coalesce(
  #                 func.sum(case((HoldingOperationTable.action == OPERATION_ACTION_BUY, HoldingOperationTable.quantity), else_=-HoldingOperationTable.quantity)),
  #                 0).label('quantity'),
  #               func.coalesce(
  #                 func.sum(case((HoldingOperationTable.action == OPERATION_ACTION_BUY, -HoldingOperationTable.expense), else_=HoldingOperationTable.expense)),
  #                 0.0).label('expense')
  #             ).select_from(HoldingTable
  #             ).join(Data.InfoTable, Data.InfoTable.code == HoldingTable.code and Data.InfoTable.type == HoldingTable.type, isouter=True
  #             ).join(HoldingOperationTable, HoldingOperationTable.holding == HoldingTable.id, isouter=True
  #             ).filter(HoldingTable.uid == uid
  #             ).group_by(HoldingTable.id
  #             ).order_by(HoldingTable.updated.desc())
  stmt = select(HoldingTable,
                Data.InfoTable.name.label('name'),
                func.coalesce(
                  func.sum(HoldingOperationTable.quantity),
                  0).label('quantity'),
                func.coalesce(
                  func.sum(HoldingOperationTable.expense),
                  0.0).label('expense')
              ).select_from(HoldingTable
              ).join(Data.InfoTable, and_(Data.InfoTable.code == HoldingTable.code, Data.InfoTable.type == HoldingTable.type), isouter=True
              ).join(HoldingOperationTable, HoldingOperationTable.holding == HoldingTable.id, isouter=True
              ).filter(HoldingTable.uid == uid
              ).group_by(HoldingTable.id
              ).order_by(HoldingTable.updated.asc())  

  stmt = stmt.where(HoldingOperationTable.action != OPERATION_ACTION_SOLDOUT)

  if id:
    stmt = stmt.where(HoldingTable.id == id)
  if type:
    stmt = stmt.where(HoldingTable.type == type)
  if code:
    stmt = stmt.where(HoldingTable.code == code)
  if flag:
    stmt = stmt.where(HoldingTable.flag == flag)
  
  # print(str(stmt))
  results = dbEngine.select_stmt(stmt)
  
  ret: list[UserHoldingRecord] = []
  for r in results:
    ret.append(UserHoldingRecord(
      id=r[0].id,
      type=r[0].type,
      code=r[0].code,
      name=r[1],
      flag=r[0].flag,
      created=r[0].created,
      updated=r[0].updated,
      quantity=r[2],
      expense=r[3]
    ))
  return ret

def get_holding_summary(holding_id: int) -> (int, float):
  """
  Get the summary of a holding.
  Returns a tuple of (quantity, expense).
  """
  stmt = select(
      func.coalesce(func.sum(HoldingOperationTable.quantity), 0).label('quantity'),
      func.coalesce(func.sum(HoldingOperationTable.expense), 0.0).label('expense')
  ).where(HoldingOperationTable.holding == holding_id)
  
  results = dbEngine.select_stmt(stmt)
  if results:
      result = results[0]
      return result.quantity, result.expense
  return 0, 0.0

