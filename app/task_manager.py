"""
系统任务管理
"""
import os
from enum import Enum
from datetime import datetime, timedelta
import pickle

from app.dbengine import engine, text
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.combining import AndTrigger

from app import AppException, logger

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
    
    def restore_job(self, id: str, trigger: dict, func: callable, args: dict = None) -> str:
        id = args['id']
        trig = self.make_trigger(trigger)
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

PATH_TASK_INSTANCE = './app/db/instance' # 'app\\db\\instance'
TABLE_TASK_INSTANCE = 'sys_task_instance'

class TaskType(Enum):
    All = 0
    FinderStrategyInstance = 1
    PipeFinderStrategyInstance = 2
    SysDataInstance = 3
    SysWatchInstance = 4
    FetchDataInstance = 5

class Task:
    def __init__(self, type: TaskType, id: str, trigger: dict, func: callable, attach: dict = None) -> None:
        self.type = type
        self.id = id
        self.trigger = trigger
        self.func = func
        # self.args = args
        self.attach = attach
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
        self.load_tasks()
    
    def shutdown(self) -> None:
        # self.save()
        self.scheduler.shutdown()

    def create(self, type: TaskType, trigger: dict, func: callable, args: dict = None, attach: dict = None) -> str:
        id = self.scheduler.make_job(trigger=trigger, func=func, args=args)
        if attach is None:
            attach = {}
        attach['args'] = args
        self.taskList[id] = Task(type, id, trigger, func, attach)

        # self.save_task(self.taskList[id])
        return id
    
    def create_task(self, task: Task) -> str:
        args = task.attach['args']
        id = args['id']
        self.scheduler.restore_job(id=id, trigger=task.trigger, func=task.func, args=args)
        self.taskList[id] = task

        return id

    def remove(self, id) -> str:
        self.scheduler.remove_job(id)
        self.taskList.pop(id, None)

        self.delete_task(id)
        return id
    
    def get_jobs(self) -> list:
        return self.scheduler.jobs()

    def get(self, id: str) -> Task | None:
        return self.taskList.get(id, None)
    
    def get_with_type(self, type: TaskType, id: str | None = None, attach: tuple[str, ...] | None = None) -> Task | list[Task] | None:
        ret: list[Task] = []
        if id is None and attach is None:
            for k, v in self.taskList.items():
                if v.type == type or v.type == TaskType.All:
                    ret.append(v)
        elif id is None and attach:
            for k, v in self.taskList.items():
                if v.type == type or v.type == TaskType.All:
                    if v.attach:
                        if attach[0] in v.attach and attach[1] == v.attach[attach[0]]:
                            ret.append(v)
        else:
            ret = self.get(id)
        return ret
        
    def get_finder_strategy(self, id: str | None, attach: tuple[str, ...] | None = None) -> Task | list[Task] | None:
        return self.get_with_type(TaskType.FinderStrategyInstance, id, attach)
    
    def get_pipe_finder_strategy(self, id: str | None) -> Task | list[Task] | None:
        return self.get_with_type(TaskType.PipeFinderStrategyInstance, id)

    def set_result(self, id: str, result: any, duration: timedelta = None) -> str | None:
        task = self.taskList.get(id, None)
        if task is None:
            return None
        task.result = result
        task.runTimes += 1
        task.lastUpdated = datetime.now()
        task.duration = duration

        return self.update_task(task)

    def set_trigger(self, id: str, trigger: dict) -> str | None:
        task = self.taskList.get(id, None)
        if task is None:
            return None        
        self.scheduler.reschedule_job(id, trigger)
        task.trigger = trigger
        return self.update_task(task)

    def create_finder_strategy(self, title: str, func: callable, trigger: dict, strategy: str, args: dict = None) -> str:
        id =  self.create(TaskType.FinderStrategyInstance, trigger, func, args, {
            'title': title,
            'strategy': strategy,           
        })

        self.save_task(self.taskList[id])
        return id
    
    def create_pipe_finder_strategy(self, title: str, func: callable, trigger: dict, strategies: list) -> str:
        args = {
            'strategies': strategies
        }
        id = self.create(TaskType.PipeFinderStrategyInstance, trigger, func, args, {
            'title': title,       
        })
        self.save_task(self.taskList[id])
        return id
    
    def create_fetch_data(self, func: callable, args: dict = None, seconds=2) -> str:
        trigger = {
            'mode': 'delay',
            'seconds': seconds 
        }
        id = self.create(TaskType.FetchDataInstance, trigger, func, args)
        self.save_task(self.taskList[id])
        return id

    def __load_task(self, id: str) -> str:
        file = self.__make_task_local(id)
        with open(file, 'rb') as input:
            task = pickle.load(input)
            return self.create_task(task)

    def load_tasks(self) -> None:
        try:
            stmt = text(f'SELECT id FROM {TABLE_TASK_INSTANCE}') # select(TABLE_TASK_INSTANCE)
            with engine.connect() as conn:
                results = conn.execute(stmt)
                for row in results:
                    self.__load_task(row.id)
        except Exception as e:
            raise AppException(e)

    def __make_task_local(self, id: str) -> str:
        return f'{PATH_TASK_INSTANCE}\\{id}.i'

    def save_task(self, task: Task) -> str:
        try:
            file = self.__make_task_local(task.id)
            with open(file, 'wb') as output:
                pickle.dump(task, output)

            data = {
                "id": task.id
            }

            stmt = text(f'INSERT INTO {TABLE_TASK_INSTANCE}(id) VALUES(:id)')
            with engine.connect() as conn:
                conn.execute(stmt, data)
                conn.commit()
            
            return task.id
        except Exception as e:
            raise AppException(e)    

    def delete_task(self, id: str) -> str:
        try:
            data = {
                "id": id
            }
            stmt = text(f'DELETE FROM {TABLE_TASK_INSTANCE} WHERE id==:id')
            with engine.connect() as conn:
                conn.execute(stmt, data)
                conn.commit()
            file = self.__make_task_local(id)
            os.remove(file)
        except Exception as e:
            raise AppException(e)

    def update_task(self, task: Task) -> str:
        try:
            file = self.__make_task_local(task.id)
            with open(file, 'wb') as output:
                pickle.dump(task, output)
            return task.id
        except Exception as e:
            raise AppException(e)                  


taskManager = TaskManager() 