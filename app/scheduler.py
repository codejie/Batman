from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.combining import AndTrigger

from app import logger

class Scheduler:
    def __init__(self):
        self._scheduler = BackgroundScheduler()

    def start(self):
        self._scheduler.start()

    def shutdown(self):
        self._scheduler.shutdown(True)

    def addJob(self, **kwargs) -> str:
        # logger.debug(kwargs)

        func: callable = kwargs['func']
        name: str = kwargs['title']
        # id: str = kwargs['id']
        mode: str = kwargs['mode']
        days: str = kwargs['days'] # '0-4' or 'mon,tue,wed,thu,fri'
        hour: int = kwargs['hour']
        minute: int = kwargs['minute']
        args: dict = kwargs['args']
        trigger: CronTrigger = CronTrigger(day_of_week=days, hour=hour, minute=minute)
        job = self._scheduler.add_job(func=func, kwargs=args, trigger=trigger, name=name)

        logger.debug(f'schedule job - \n{job}')

        return job.id

    def removeJob(self, id: str):
        self._scheduler.remove_job(id)

scheduler = Scheduler()

