"""
Stock本地化函数
"""
from pandas import DataFrame

from app.utils import debug

from app.logger import logger
from app.exception import AppDataException
from app.data.remote_api import stock as remote
from app.database import dbEngine
from app.database.tables import TableName

def fetch_a_stock(if_exists: str) -> None:
    logger.debug(f'{debug.__function__()}() called')
    df = remote.get_a_code()
    df.to_sql(TableName.Stock_A_List, dbEngine, if_exists=if_exists, index=False)
    logger.debug(f'{debug.__function__()}() called end')