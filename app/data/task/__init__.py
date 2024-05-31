"""
System Data Initialization
"""
from datetime import datetime
from app.logger import logger

from app.data.task import stock
from app.task_manager import Task, TaskType, taskManager

def init() -> None:
    logger.info('system data init check, maybe would take a long time..')
    stock.init_check()
    logger.info('system data init check end')

def daily_update_check(**kwargs) -> None:
    now = datetime.now()
    if (now.hour >= 9 and now.hour < 16) or now.weekday() > 4:
        logger.info('daily update check process skip..')
        return
    logger.info('daily update check start..')
    stock.update_daily()
    logger.info('daily update check end.')

def update_task() -> None:
    # daily update task
    trigger = {
        'mode': 'interval',
        'seconds': 10800
    }

    task = Task(type=TaskType.DataCheck,
                trigger=trigger,
                func=daily_update_check,
                args=None)
    id = taskManager.push(task=task, need_save=False)
    logger.info(f'register daily update task - {id}')