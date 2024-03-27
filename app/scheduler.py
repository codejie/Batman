from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.combining import AndTrigger
from datetime import datetime, timedelta

# from app.routers.strategy.local_cache import createFinderStrategyInstance

from app import logger

class Scheduler:
    def __init__(self):
        self._scheduler = BackgroundScheduler()

    def start(self):
        self._scheduler.start()

    def shutdown(self):
        self._scheduler.shutdown(True)
    
    def makeJobId(self) -> str:
        return datetime.today().strftime('%Y%m%d%H%M%S%f')

    def addFinderStrategyJob(self, **kwargs) -> str | None:
        # logger.debug(kwargs)

        # strategy = kwargs['strategy']
        func: callable = kwargs['func']
        name: str = kwargs['title']
        trigger: dict = kwargs['trigger']
        args: dict = kwargs['args']

        mode: str = trigger['mode'] # kwargs['mode']
        days: str = trigger['days'] # '0-4' or 'mon,tue,wed,thu,fri'
        hour: int = trigger['hour']
        minute: int = trigger['minute']

        # trigger: CronTrigger = CronTrigger(day_of_week=days, hour=hour, minute=minute)
        id = self.makeJobId()
        args['id'] = id
        job = self._scheduler.add_job(func=func, kwargs=args, trigger=CronTrigger(day_of_week=days, hour=hour, minute=minute), name=name, id=id)

        # createFinderStrategyInstance(id, name, trigger, strategy, args)

        logger.debug(f'schedule job - \n{job}')

        return job.id

    def addDailyJob(self, func: callable, days: str, hour: int, minute: int) -> str:
        pass

    def addIntervalJob(self, func: callable, interval: int) -> str:
        id = self.makeJobId()
        trigger = IntervalTrigger(seconds=interval)
        args = {
            'id': id
        }
        job = self._scheduler.add_job(id=id, trigger=trigger, func=func, kwargs=args)
        return job.id
    
    def addDelayJob(self, func: callable, seconds: int) -> str:
        id = self.makeJobId()
        t = datetime.now() + timedelta(seconds=seconds)
        trigger = CronTrigger(year=t.year, month=t.month, day=t.day, hour=t.hour, minute=t.minute, second=t.second)
        args = {
            'id': id
        }
        job = self._scheduler.add_job(id=id, trigger=trigger, func=func, kwargs=args)
        return job.id

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
    
    def listJobs(self) -> list:
        ret = []
        for job in self._scheduler.get_jobs():
            ret.append({
                'id': job.id,
                'trigger': f'{job.trigger}',
                'next run at': f'{job.next_run_time}'
            })
        
        return ret

scheduler = Scheduler()

