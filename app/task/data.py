"""
数据任务
"""
from app import logger
from app.dbengine import engine
from app.data.local_db import stock

options: dict = {
    'codes': None,
    'start': '',
    'end': '',
    'if_exists': 'append'
}

def checkStockData(start: str, end: str) -> None:
    
    pass

"""
incoude:
    stock history
    stock hsgt
    stock margin
"""
def updateDailyStockData():
    try:
        stock.fetch_history(symbol=options['codes'], start=options['start'], end=options['end'], period='daily', adjust='qfq', if_exists=options['if_exits'])

        stock.fetch_hsgt(symbol=options['codes'], start=options['start'], end=options['end'], if_exists='replace') # options['if_exits'])

        stock.fetch_margin(symbol=options['codes'], start=options['start'], end=options['end'], if_exists=options['if_exits'])
    except Exception as e:
        logger.warn(f'updateDailyStockData() fail - {e}')