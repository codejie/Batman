"""
每日数据下载
"""
from enum import Enum
from datetime import datetime, timedelta

from app import logger, utils
from app.dbengine import engine, text
from app.data.local_db import stock


    
def check(**kwargs):
    logger.info('fetch_daily_data check() start.')
    # STOCK_DIALIY_HISTORY
    fetch_stock_history(**kwargs)

    logger.info('fetch_daily_data check() end.')

def fetch_stock_history(**kwargs):
    logger.info('-- fetch_stock_history() start.')

    


    logger.info('-- fetch_stock_history() end.')

