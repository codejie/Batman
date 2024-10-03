"""
System Data Initialization
"""
from datetime import datetime
from app.logger import logger

from app.data.task import stock, index, stock_third
from app.task_scheduler import taskScheduler
from app import config

def init() -> None:
    logger.info('system data init check, maybe would take a long time..')
    stock.init_check()
    index.init_check()
    logger.info('system data init check end')

def update_task() -> None:
  register_update_daily()
  register_update_third()

def daily_update_check(**kwargs) -> None:
  try:
    # now = datetime.now()
    # if (now.hour >= 9 and now.hour < 16): #  or now.weekday() > 4:
    #     logger.info('daily update check process skip..')
    #     return
    logger.info('daily update check start..')
    stock.update_daily()
    index.update_daily()
    logger.info('daily update check end.')
  except Exception as e:
    logger.info(f'daily update check failed - {str(e)}')

def register_update_daily():
  # daily update task
  trigger = config.UPDATE_DAILY_TRIGGER
  id = taskScheduler.make_id()
  taskScheduler.make_job(id=id, trigger=trigger, func=daily_update_check, args=None)
  logger.info(f'register daily update task - {id}')

def daily_update_third_check(**kwargs) -> None:
  try:
    logger.info('daily update third data start..')
    stock_third.update_daily()
    logger.info('daily update third data end.')
  except Exception as e:
    logger.info(f'daily update third data fail - {str(e)}')

def register_update_third():
  trigger = config.UPDATE_DAILY_THIRD_TRIGGER
  id = taskScheduler.make_id()
  taskScheduler.make_job(id=id, trigger=trigger, func=daily_update_third_check, args=None)
  logger.info(f'register daily update third data task - {id}')