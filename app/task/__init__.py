"""
register daily_data_check function
"""
from app import logger
from app.task_manager import taskManager, TaskType
from app.task.fetch_init_data import init_check
from app.task.fetch_daily_data import fetch_data as fetch_daily_data

def register_daily_data_check():
    # trigger = {
    #     'mode': 'daily',
    #     'days': '0-6',
    #     'hour': 19,
    #     'minute': 36
    # }

    trigger = {
        'mode': 'interval',
        'seconds': 3600
    }

    id = taskManager.create(type=TaskType.SysDataInstance,
                       trigger=trigger,
                       func=fetch_daily_data,
                       args=None)
    logger.info(f'register_daily_data_check() - {id}')


def register_system_check():
    register_daily_data_check()