"""
register daily_data_check function
"""
from app import logger
from app.task_manager import taskManager, TaskType
from app.task.daily_data_check import system_daily_data_updated_check

def register_daily_data_check():
    trigger = {
        'mode': 'daily',
        'days': '0-6',
        'hour': 13,
        'minute': 38
    }

    id = taskManager.create(type=TaskType.SysDataInstance,
                       trigger=trigger,
                       func=system_daily_data_updated_check,
                       args=None)
    logger.info(f'register_daily_data_check() - {id}')


def register_system_check():
    register_daily_data_check()