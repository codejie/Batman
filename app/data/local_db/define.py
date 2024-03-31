"""
Table Name definition
"""

# TableName = {
#     'A_Stock': 'table_a_stock'
# }

class TableName:
    A_Stock = 'table_a_stock'

    @staticmethod
    def make_stock_history_name(symbol: str, period: str = 'daily', adjust: str = 'qfq') -> str:
        return f'table_{symbol}_{period}_{adjust}'