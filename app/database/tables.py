"""
All Table definitions
"""
from app.database import TableBase, Column, String

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

# class TableBase(DeclarativeBase):
#     pass


class StockAListTable(TableBase):
    __tablename__ = TableName.Stock_A_List

    code = Column(String, primary_key=True)
    name = Column(String)

class IndexAListTable(TableBase):
    __tablename__ = TableName.Index_A_List

    code = Column(String, primary_key=True)
    name = Column(String)
    market = Column(String)