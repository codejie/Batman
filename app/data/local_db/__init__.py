"""
Table Name definition
"""

class TableName:
    Stock_A_List = 'stock_a_list'
    Index_A_List = 'index_a_list'

    @staticmethod
    def make_stock_history_name(symbol: str, period: str = 'daily', adjust: str = 'qfq') -> str:
        return f'stock_{symbol}_{period}_{adjust}'
    
    @staticmethod
    def make_index_history_name(symbol: str, period: str = 'daily') -> str:
        return f'index_{symbol}_{period}'