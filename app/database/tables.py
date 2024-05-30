"""
All Table definitions
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase


class TableName:
    Stock_A_List = 'stock_a_list'
    Index_A_List = 'index_a_list' 

    @staticmethod
    def make_stock_history_name(symbol: str, period: str = 'daily', adjust: str = 'qfq') -> str:
        return f'stock_{symbol}_{period}_{adjust}'
    
    @staticmethod
    def make_index_history_name(symbol: str, period: str = 'daily') -> str:
        return f'index_{symbol}_{period}'
    
    @staticmethod
    def make_stock_hsgt_name(symbol: str) -> str:
        return f'stock_{symbol}_hsgt'
    
    @staticmethod
    def make_stock_margin_name(symbol: str) -> str:
        return f'stock_{symbol}_margin'

class TableBase(DeclarativeBase):
    pass

class Version(TableBase):
    __tablename__ = 'sys_infos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String)
    updated = Column(DateTime(timezone=True), server_default=func.now())

class StockAListTable(TableBase):
    __tablename__ = TableName.Stock_A_List

    code = Column(String, primary_key=True)
    name = Column(String)
