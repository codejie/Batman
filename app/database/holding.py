from datetime import datetime
from sqlalchemy import Index, ForeignKey, literal
from app.database import TableBase, Column, Integer, Float, String, DateTime, func
from app.database import dbEngine, sql_insert, sql_delete, sql_update, sql_select, and_, case

from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from app.database.tables import IndexAListTable, StockAListTable

TRADE_ACTION_BUY: int = 0
TRADE_ACTION_SELL: int = 1
HOLDING_FLAG_NORMAL: int = 0
HOLDING_FLAG_REMOVED: int = 1

class HoldingListTable(TableBase):
  __tablename__ = 'user_holding_list'

  # id = Column(Integer, autoincrement='auto', primary_key=True)
  id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
  uid = Column(Integer, nullable=False, default=99)
  type = Column(Integer, default=1)
  code = Column(String, nullable=False)
  # quantity = Column(Integer, nullable=False)
  # buying = Column(Float, nullable=False) # 买入价
  # cost = Column(Float, nullable=False) # 成本价
  # comment = Column(String, nullable=True)
  created = Column(DateTime(timezone=True), server_default=func.now())
  updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
  flag = Column(Integer, nullable=False, default=HOLDING_FLAG_NORMAL) # 0: normal, 1: removed

  __table_args__ = (
    Index('type_code_index', 'type', 'code', unique=True),
  # UniqueConstraint("type", "code", name="type_code_index")    
  )


class TradeRecordTable(TableBase):
  __tablename__ = 'user_holding_trade_record'

  id = Column(Integer, autoincrement='auto', primary_key=True)
  # uid = Column(Integer, nullable=False, default=99)
  holding = Column(Integer, ForeignKey(HoldingListTable.id), nullable=False)
  action = Column(Integer, nullable=False)
  # type = Column(Integer, default=1)
  # code = Column(String, nullable=False)
  quantity = Column(Integer, nullable=False)
  # buying = Column(Float, nullable=False)
  # selling = Column(Float, nullable=False)
  # deal = Column(Float, nullable=False) # 成交价
  expense = Column(Float, nullable=False) # 总费用
  comment = Column(String, nullable=True)
  created = Column(DateTime(timezone=True), server_default=func.now())


def insert(uid: int, type: int, code: str, quantity: int, expense: float, comment: str = None, created: datetime = func.now()) -> int:
  # stmt = sql_insert(HoldingListTable).values(
  #   uid=uid,
  #   type=type,
  #   code=code
  # )
  stmt = sqlite_insert(HoldingListTable).values(uid=uid, type=type, code=code, created=created)
  stmt = stmt.on_conflict_do_update(
    index_elements=[HoldingListTable.type, HoldingListTable.code],
    set_=dict(updated=func.now(), flag=HOLDING_FLAG_NORMAL)).return_defaults(HoldingListTable.id)
  id = dbEngine.insert(stmt=stmt)
  stmt = sql_insert(TradeRecordTable).values(
    holding=id,
    action=TRADE_ACTION_BUY,
    quantity=quantity,
    expense=expense,
    comment=comment,
    created=created
  )
  id = dbEngine.insert(stmt=stmt)
  return id

def update(uid: int, action: int, type: int, code: str, quantity: int, expense: float, comment: str = None, created: datetime = func.now()) -> int:
  # stmt = sql_insert(TradeRecordTable).from_select(
  #   [TradeRecordTable.holding, TradeRecordTable.action, TradeRecordTable.quantity,
  #    TradeRecordTable.deal, TradeRecordTable.cost, TradeRecordTable.comment],
  #    select(
  #      HoldingListTable.id,
  #      bindparam(TradeRecordTable.action, action),
  #      bindparam('quantity', quantity),
  #      bindparam('deal', deal),
  #      bindparam('code', cost),
  #      bindparam('comment', comment)
  #     ).filter(
  #      HoldingListTable.type == type, HoldingListTable.code == code
  #    )
  # )
  stmt = sql_insert(TradeRecordTable).from_select(
    names=[
      TradeRecordTable.holding,
      TradeRecordTable.action,
      TradeRecordTable.quantity,
      TradeRecordTable.expense,
      TradeRecordTable.comment,
      TradeRecordTable.created
     ],
     select=sql_select(
       HoldingListTable.id,
       action,
       quantity,
       expense,
       literal(comment),
       created
      ).filter(
       HoldingListTable.uid == uid,
       HoldingListTable.type == type,
       HoldingListTable.code == code
     )
  )
  return dbEngine.update(stmt=stmt)

def remove(uid: int, id: int) -> int:
  stmt = sql_update(HoldingListTable).values(
      flag=HOLDING_FLAG_REMOVED
    ).where(
      HoldingListTable.uid == uid and HoldingListTable.id == id
    )
  return dbEngine.update(stmt=stmt)

def test(uid: int, type: int, code: str, quantity: int, expense: float, comment: str = None) -> int:
  # stmt = sqlite_insert(HoldingListTable).values(uid=uid, type=type, code=code)
  # stmt = stmt.on_conflict_do_update(
  #   index_elements=[HoldingListTable.type, HoldingListTable.code],
  #   set_=dict(updated=func.now(), flag=1))
  # return dbEngine.insert(stmt=stmt)
  stmt = sql_select(
    # func.sum(case([(TradeRecordTable.action==TRADE_ACTION_BUY, TradeRecordTable.cost)],
    #                else_=-TradeRecordTable.cost)).label('cost')
    func.sum(TradeRecordTable.expense).label('expense'),
    func.sum(
      case((TradeRecordTable.action==TRADE_ACTION_BUY, TradeRecordTable.expense),
                   else_=-TradeRecordTable.expense)
    ).label('expense')
  ).group_by(TradeRecordTable.holding)
  results = dbEngine.select_with_execute(stmt)
  return 0


def get_holding(uid: int, type: int = None, code: str = None, with_removed: bool = False) -> list:
  stmt = sql_select(HoldingListTable,
        case(
            (HoldingListTable.type == 1, StockAListTable.name),
            else_=IndexAListTable.name
          ).label('name')
        ).select_from(
          HoldingListTable
        ).join(StockAListTable, StockAListTable.code == HoldingListTable.code, isouter=True
        ).join(IndexAListTable, IndexAListTable.code == HoldingListTable.code, isouter=True
        ).filter(
          HoldingListTable.uid == uid
        ).order_by(HoldingListTable.id)
  if (type is not None) and (code is not None):
    stmt = stmt.where(HoldingListTable.type == type, HoldingListTable.code == code)
  elif type is not None:
    stmt = stmt.where(HoldingListTable.type == type)
  elif code is not None:
    stmt = stmt.where(HoldingListTable.code == code)
  if not with_removed:
    stmt = stmt.where(HoldingListTable.flag == HOLDING_FLAG_NORMAL)

  # stmt = sql_select(HoldingListTable).where(HoldingListTable.uid == uid)
  # if (type is not None) and (code is not None):
  #   stmt = stmt.where(HoldingListTable.type == type, HoldingListTable.code == code)
  # elif type is not None:
  #   stmt = stmt.where(HoldingListTable.type == type)
  # elif code is not None:
  #   stmt = stmt.where(HoldingListTable.code == code)
  # if not with_removed:
  #   stmt = stmt.where(HoldingListTable.flag == HOLDING_FLAG_NORMAL)

  results = dbEngine.select_with_execute(stmt)
  ret = []
  for r in results:
    ret.append({
      'id': r[0].id,
      'name': r[1],
      'type': r[0].type,
      'code': r[0].code,
      'created': r[0].created,
      'updated': r[0].updated,
      'flag': r[0].flag
    })

  return ret

def get_record(uid: int, holding: int = None, action: int = None, with_removed: bool = False) -> list:
  stmt = sql_select(
    TradeRecordTable
  ).join(HoldingListTable, TradeRecordTable.holding == HoldingListTable.id
  ).filter(HoldingListTable.uid == uid
  ).order_by(TradeRecordTable.id.desc())
  
  if holding is not None:
    stmt = stmt.where(TradeRecordTable.holding == holding)
  if action is not None:
    stmt = stmt.where(TradeRecordTable.action == action)
  if not with_removed:
    stmt = stmt.where(HoldingListTable.flag == HOLDING_FLAG_NORMAL)

  results = dbEngine.select_with_execute(stmt)
  ret = []
  for r in results:
    ret.append({
      'id': r[0].id,
      'holding': r[0].holding,
      'action': r[0].action,
      'quantity': r[0].quantity,
      'expense': r[0].expense,
      'comment': r[0].comment,
      'created': r[0].created,
    })  
  return ret

def calc_holding(uid:int, type: int = None, code: str = None, with_removed: bool = False) -> list:
  stmt = sql_select(HoldingListTable,
          case(
            (HoldingListTable.type == 1, StockAListTable.name),
            else_=IndexAListTable.name
          ).label('name'),
          func.sum(case((TradeRecordTable.action==TRADE_ACTION_BUY, TradeRecordTable.quantity),
                   else_=-TradeRecordTable.quantity)).label('quantity'),
          func.sum(case((TradeRecordTable.action==TRADE_ACTION_SELL, TradeRecordTable.expense),
                   else_=-TradeRecordTable.expense)).label('expense'),
        ).select_from(
          HoldingListTable
        ).join(StockAListTable, StockAListTable.code == HoldingListTable.code, isouter=True
        ).join(IndexAListTable, IndexAListTable.code == HoldingListTable.code, isouter=True
        ).join(TradeRecordTable, TradeRecordTable.id == HoldingListTable.id, isouter=True
        ).filter(
          HoldingListTable.uid == uid
        ).group_by(HoldingListTable.type, HoldingListTable.code
        ).order_by(HoldingListTable.id)
  
  if (type is not None) and (code is not None):
    stmt = stmt.where(HoldingListTable.type == type, HoldingListTable.code == code)
  elif type is not None:
    stmt = stmt.where(HoldingListTable.type == type)
  elif code is not None:
    stmt = stmt.where(HoldingListTable.code == code)
  if not with_removed:
    stmt = stmt.where(HoldingListTable.flag == HOLDING_FLAG_NORMAL)
  results = dbEngine.select_with_execute(stmt)

  ret = []
  for r in results:
    ret.append({
      'id': r[0].id,
      'name': r[1],
      'type': r[0].type,
      'code': r[0].code,
      'created': r[0].created,
      'updated': r[0].updated,
      'flag': r[0].flag,
      'quantity': r[2],
      'expense': r[3]
    })

  return ret

# 收益 = sum(expense)
# 成本价 = sum(expense) / sum(quantity)
# 市值 = sum(quantity) * price
# 盈亏 = sum(expense) - 市值
