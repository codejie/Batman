"""
System Data Initialization
"""

from app.logger import logger

from app.data.task.update import stock

def init() -> None:
    logger.info('system data init, maybe would take a long time..')
    stock.init_check()
    logger.info('system data init end')

def update() -> None:
    pass