"""
Stock & Index Information Table
"""

from typing import Optional
from sqlalchemy import Column, Index, Integer, PrimaryKeyConstraint, String, select
from app.database import TableBase, dbEngine


ITEM_TYPE_INDEX: int = 1
ITEM_TYPE_STOCK: int = 2

class InfoTable(TableBase):
  __tablename__ = 'item_info_table'

  type = Column(Integer, nullable=False, default=ITEM_TYPE_STOCK)
  code = Column(String, nullable=False)
  name = Column(String, nullable=False)
  market = Column(String, nullable=True)

  __table_args__ = (
      PrimaryKeyConstraint('type', 'code', name='pk_info_type_code'),
  )

def select_name(code: str, type: int = ITEM_TYPE_STOCK) -> Optional[str]:
  stmt = select(InfoTable.name, InfoTable.type).where(InfoTable.type == type).where(InfoTable.code == code)
  result = dbEngine.select_scalar(stmt)
  return result[0] if result else None