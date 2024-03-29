"""
Scheduler Job definition
"""

from app import logger, AppException
from app.scheduler import scheduler
from app.dbengine import engine
from app.data import stock

from app.data.local_db.define import TableName

def fetchAStock() -> str:
    def func(**kwargs):
        logger.debug('fetchAStock() start.')
        df = stock.get_a_code()
        df.to_sql(TableName['A_Stock'], engine, if_exists='replace')
        logger.debug('fetchAStock() end.')

    return scheduler.addDelayJob(func=func, args={}, seconds=2)

async def scheduleFetchJob(name: str) -> str:
    if name == 'fetch_a_stock':
        return fetchAStock()
    else:
        raise AppException(code=-1, message=f'Unknown job name - {name}')