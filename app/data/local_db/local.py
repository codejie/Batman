"""
访问本地数据的函数集合
"""

import pandas as pd

from app.dbengine import engine
from app.data.local_db.define import TableName

def get_a_code(market: str | None = None) -> pd.DataFrame:
    return pd.read_sql_table(TableName['A_Stock'], engine)
    