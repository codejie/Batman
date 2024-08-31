"""
System Data Initialization
"""
from datetime import datetime
from app.logger import logger

from app.data.task import stock
from app.task_scheduler import taskScheduler

# UPDATE_TASK_RUNNING: bool = False

def init() -> None:
    logger.info('system data init check, maybe would take a long time..')
    stock.init_check()
    logger.info('system data init check end')

def daily_update_check(**kwargs) -> None:
    # global UPDATE_TASK_RUNNING
    # if UPDATE_TASK_RUNNING:
    #    logger.info('Daily update is running, skip..')
    #    return
    
    # UPDATE_TASK_RUNNING = True
    now = datetime.now()
    if (now.hour >= 9 and now.hour < 16) or now.weekday() > 4:
        logger.info('daily update check process skip..')
        return
    logger.info('daily update check start..')
    stock.update_daily()
    logger.info('daily update check end.')
    # UPDATE_TASK_RUNNING = False

def test(**kwargs) -> None:
   logger.debug(datetime.now())

def update_task(for_test: bool = False) -> None:
    # FOR TEST
    if for_test:
      logger.info('daily update check start..')
      stock.update_daily()
      logger.info('daily update check end.')
    else:
    # daily update task
      trigger = {
          # 'mode': 'interval',
          # 'seconds': 3600 * 4
        'mode': 'daily',
        'days': '0-5',
        'hour': 23,
        'minute': 29          
      }
      id = taskScheduler.make_id()
      taskScheduler.make_job(id=id, trigger=trigger, func=daily_update_check, args=None)
      logger.info(f'register daily update task - {id}')