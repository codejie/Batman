"""
系统任务管理
"""
from enum import Enum
from datetime import datetime, timedelta
import _pickle as pickle

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.combining import AndTrigger

from app import AppException

"""
Scheduler
"""
class TriggerMode(Enum):
    Daily = 'daily'
    Delay = 'delay'
    Interval = 'interval'

class Scheduler:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown(True)
    
    def make_job_id(self) -> str:
        return datetime.today().strftime('%Y%m%d%H%M%S%f')

    def make_trigger(self, trigger: dict) -> BaseTrigger:
        mode = trigger['mode']
        if mode == TriggerMode.Daily.value:
            return CronTrigger(day_of_week=trigger['days'], hour=trigger['hour'], minute=trigger['minute'])
        elif mode == TriggerMode.Delay.value:
            t = datetime.now() + timedelta(seconds=int(trigger['seconds']))
            return CronTrigger(year=t.year, month=t.month, day=t.day, hour=t.hour, minute=t.minute, second=t.second)
        elif mode == TriggerMode.Interval.value:
            return IntervalTrigger(seconds=int(trigger['seconds']))
        else:
            raise AppException(message=f'unknown trigger mode - {mode}')

    def make_job(self, trigger: dict, func: callable, args: dict = None) -> str:
        id = self.make_job_id()
        trig = self.make_trigger(trigger)
        if args is None:
            args = {}
        args['id'] = id
        job = self.scheduler.add_job(id=id, trigger=trig, func=func, kwargs=args)
        return job.id
    
    def remove_job(self, id: str):
        self.scheduler.remove_job(id)

    def reschedule_job(self, id: str, trigger: dict) -> str:
        trig = self.make_trigger(trigger)
        self._cheduler.reschedule_job(job_id=id, trigger=trig)
        return id
    
    def jobs(self) -> list:
        ret = []
        for job in self.scheduler.get_jobs():
            ret.append({
                'id': job.id,
                'trigger': f'{job.trigger}',
                'next run at': f'{job.next_run_time}'
            })
        
        return ret

"""
TaskManager
"""
class TaskType(Enum):
    All = 0
    FinderStrategyInstance = 1
    PipeFinderStrategyInstance = 2
    SysDataInstance = 3
    SysWatchInstance = 4
    FetchDataInstance = 5

class Task:
    def __init__(self, type: TaskType, id: str, trigger: dict, element: dict) -> None:
        self.type = type
        self.id = id
        self.trigger = trigger
        self.element = element
        self.runTimes = 0
        self.lastUpdated = None
        self.duration = None
        self.result = None

class TaskManager:
    def __init__(self) -> None:
        self.taskList: dict[str, Task] = {}
        self.scheduler = Scheduler()
    
    def start(self) -> None:
        self.scheduler.start()
        self.load()
    
    def shutdown(self) -> None:
        self.save()
        self.scheduler.shutdown()

    def create(self, type: TaskType, trigger: dict, func: callable, args: dict = None, attachment: dict = None) -> str:
        id = self.scheduler.make_job(trigger=trigger, func=func, args=args)
        if attachment is None:
            attachment = {}
        attachment['args'] = args
        self.taskList[id] = Task(type, id, trigger, attachment)
        return id
    
    def remove(self, id) -> str:
        self.scheduler.remove_job(id)
        self.taskList.pop(id, None)
        return id
    
    def get_jobs(self) -> list:
        return self.scheduler.jobs()

    def get(self, id: str) -> Task | None:
        return self.taskList.get(id, None)
    
    def get_type(self, type: TaskType, id: str | None) -> Task | list[Task] | None:
        if id is None:
            ret: list[Task] = []
            for k, v in self.taskList.items():
                if v.type == type or v.type == TaskType.All:
                    ret.append(v)
            return ret
        else:
            return self.get(id)
        
    def get_finder_strategy(self, id: str | None) -> Task | list[Task] | None:
        return self.get_type(TaskType.FinderStrategyInstance, id)
    
    def get_pipe_finder_strategy(self, id: str | None) -> Task | list[Task] | None:
        return self.get_type(TaskType.PipeFinderStrategyInstance, id)

    def set_result(self, id: str, result: any, duration: timedelta = None) -> str | None:
        task = self.taskList.get(id, None)
        if task is None:
            return None
        task.result = result
        task.runTimes += 1
        task.lastUpdated = datetime.now()
        task.duration = duration
        return id

    def set_trigger(self, id: str, trigger: dict) -> str | None:
        task = self.taskList.get(id, None)
        if task is None:
            return None        
        self.scheduler.reschedule_job(id, trigger)
        task.trigger = trigger
        return id

    def create_finder_strategy(self, title: str, func: callable, trigger: dict, strategy: str, args: dict = None) -> str:
        return self.create(TaskType.FinderStrategyInstance, trigger, func, args, {
            'title': title,
            'strategy': strategy,           
        })
    
    def create_pipe_finder_strategy(self, title: str, func: callable, trigger: dict, strategies: list) -> str:
        args = {
            'strategies': strategies
        }
        return self.create(TaskType.PipeFinderStrategyInstance, trigger, func, args, {
            'title': title,       
        })
    
    def create_fetch_data(self, func: callable, args: dict = None, seconds=2) -> str:
        trigger = {
            'mode': 'delay',
            'seconds': seconds
        }
        return self.create(TaskType.FetchDataInstance, trigger, func, args)
    
    def load(self) -> None:
        pass

    def save(self) -> None:
        for task in self.taskList:
            j = json.dumps(task)
            print(j)

taskManager = TaskManager() 