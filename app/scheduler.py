from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.combining import AndTrigger
from datetime import datetime

from app.routers.strategy.local_cache import createFinderStrategyInstance

from app import logger

class Scheduler:
    def __init__(self):
        self._scheduler = BackgroundScheduler()

    def start(self):
        self._scheduler.start()

    def shutdown(self):
        self._scheduler.shutdown(True)

    def addFinderStrategyJob(self, **kwargs) -> str | None:
        # logger.debug(kwargs)

        strategy = kwargs['strategy']
        func: callable = kwargs['func']
        name: str = kwargs['title']
        trigger: dict = kwargs['trigger']
        args: dict = kwargs['args']

        mode: str = trigger['mode'] # kwargs['mode']
        days: str = trigger['days'] # '0-4' or 'mon,tue,wed,thu,fri'
        hour: int = trigger['hour']
        minute: int = trigger['minute']

        # trigger: CronTrigger = CronTrigger(day_of_week=days, hour=hour, minute=minute)
        id = datetime.today().strftime('%Y%m%d%H%M%S%f')
        args['id'] = id
        job = self._scheduler.add_job(func=func, kwargs=args, trigger=CronTrigger(day_of_week=days, hour=hour, minute=minute), name=name, id=id)

        createFinderStrategyInstance(id, name, trigger, strategy, args)

        logger.debug(f'schedule job - \n{job}')

        return job.id

    def addFetchDataJob(self, **kwargs) -> str:
        pass

    def removeJob(self, id: str):
        self._scheduler.remove_job(id)

    def rescheduleJob(self, id: str, trigger: dict) -> bool:
        mode: str = trigger['mode'] # kwargs['mode']
        days: str = trigger['days'] # '0-4' or 'mon,tue,wed,thu,fri'
        hour: int = trigger['hour']
        minute: int = trigger['minute']

        trigger=CronTrigger(day_of_week=days, hour=hour, minute=minute)

        self._scheduler.reschedule_job(job_id=id, trigger=trigger)

        return True

scheduler = Scheduler()

