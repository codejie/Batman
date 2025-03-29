# """
# Stock & Index Information Table
# """

# from typing import Optional
# from sqlalchemy import Column, Index, Integer, PrimaryKeyConstraint, String, select
# from app.database import TableBase, dbEngine
# import akshare as ak


# ITEM_TYPE_INDEX: int = 1
# ITEM_TYPE_STOCK: int = 2

# class InfoTable(TableBase):
#   __tablename__ = 'item_info_table'

#   type = Column(Integer, nullable=False, default=ITEM_TYPE_STOCK)
#   code = Column(String, nullable=False)
#   name = Column(String, nullable=False)
#   market = Column(Integer, nullable=True, default=0)

#   __table_args__ = (
#       PrimaryKeyConstraint('type', 'code', name='pk_info_type_code'),
#   )

# def select_name(code: str, type: int = ITEM_TYPE_STOCK) -> Optional[str]:
#   stmt = select(InfoTable.name, InfoTable.type).where(InfoTable.type == type).where(InfoTable.code == code)
#   result = dbEngine.select_scalar(stmt)
#   return result[0] if result else None

# """
# download stock info with AKShare
# """
# def download_stock_info():
#   stock_info = ak.stock_info_a_code_name()
#   stock_info['type'] = ITEM_TYPE_STOCK
#   stock_info['market'] = None
#   data = stock_info.to_dict(orient='records')
#   dbEngine.bulk_insert_data(InfoTable, data)