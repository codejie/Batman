"""
系统任务管理
"""
import os
from enum import Enum
from datetime import datetime, timedelta
import pickle
from typing import overload

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.database import dbEngine, select, delete, insert
from app.database.tables import TableBase, Column, String, Integer, DateTime, func
from app.exception import AppException

from sqlalchemy.orm import Session

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
        trigger = self.make_trigger(trigger)
        job = self.scheduler.add_job(id=id, trigger=trigger, func=func, kwargs=args)
        return job.id        

    def remove_job(self, id: str):
        self.scheduler.remove_job(id)
        self.scheduler.modify

    def reschedule_job(self, id: str, trigger: dict) -> str:
        trig = self.make_trigger(trigger)
        self.scheduler.reschedule_job(job_id=id, trigger=trig)
        return id
    
    def run_job(self, id: str) -> str:
        self.scheduler.modify_job(id, next_run_time=datetime.now())
        return id
    
    def jobs(self) -> list:
        ret = []
        for job in self.scheduler.get_jobs():
            ret.append({
                'id': job.id,
                'trigger': f'{job.trigger}',
                'next_run': f'{job.next_run_time}'
            })
        return ret

"""
TaskManager
"""

PATH_TASK_INSTANCE = './app/db/instance' # 'app\\db\\instance'
TABLE_TASK_INSTANCE = 'sys_task_instance'

class TaskInstanceTable(TableBase):
    __tablename__ = 'sys_task_instance'

    id = Column(String, primary_key=True)
    type = Column(Integer, nullable=False)
    version = Column(String, default='1', nullable=False)
    updated = Column(DateTime(timezone=True), server_default=func.now())

    # def __str__(self) -> str:
    #     return f'{self.id}'

class TaskType(Enum):
    All = 0
    DataCheck = 1
    StrategyInstance = 20
    PipeStrategyInstance = 21

class TaskStatus(Enum):
    Normal = 0
    Paused = 1

class Task:
    def __init__(self, type: TaskType, trigger: dict, func: callable, args: dict | None = None) -> None:
        self.id = None
        self.status = TaskStatus.Normal
        self.type = type
        self.trigger = trigger
        self.func = func
        self.args = args
        self.runTimes = 0
        self.lastUpdated = None
        self.duration = None

    def set_id(self, id: str) -> None:
        self.id = id

class DataTask(Task):
    def __init__(self, trigger: dict, func: callable, args: dict | None = None) -> None:
        super().__init__(TaskType.FetchData, None, trigger, func, args)

class StrategyTask(Task):
    def __init__(self, trigger: dict, title: str, strategy: str, func: callable, args: dict | None = None) -> None:
        super().__init__(TaskType.StrategyInstance, None, trigger, func, args)
        self.title = title
        self.strategy = strategy
        self.result = None

class PipeStrategyTask(Task):
    def __init__(self, id: str, title: str, strategies: list[str], trigger: dict, func: callable, args: dict | None = None) -> None:
        super().__init__(TaskType.PipeStrategyInstance, id, trigger, func, args)
        self.title = title
        self.strategies = strategies
        self.result = None

class TaskManager:
    def __init__(self) -> None:
        self.taskList: dict[str, Task] = {}
        self.scheduler = Scheduler()
    
    def start(self) -> None:
        def callback(task: Task) -> None:
            self.taskList[task.id] = task

        self.__load_tasks(callback=callback)
        self.scheduler.start()
    
    def shutdown(self) -> None:
        self.scheduler.shutdown()

    def push(self, task: Task, need_save: bool = True) -> str:
        id = self.scheduler.make_job(trigger=task.trigger, func=task.func, args=task.args)
        task.set_id(id)
        self.taskList[task.id] = task
        if need_save:
            return self.__save_task(task)
        else:
            return task.id
    
    def pop(self, id: str) -> str | None:
        self.scheduler.remove_job(id)
        self.taskList.pop(id, None)
        return self.__remove_task(id)
    
    @overload
    def get(self, id: str) -> Task | None:
        return self.taskList.get(id, None)
    
    @overload
    def get(self, type: TaskType, **kwargs) -> list[Task]:
        ret: list[Task] = []
        for key, value in self.taskList.items():
            if value.type == type or value.type == TaskType.All:
                match = True
                for k, v in kwargs.items():
                    if getattr(value, k) != v:
                        match = False
                        break
                if match:
                    ret.append(value)
        return ret      

    def run(self, id: str) -> str | None:
        return self.scheduler.run_job(id)

    def pause(self, id) -> str | None:
        task = self.get(id)
        if task:
            self.scheduler.remove_job(id)
            task.status = TaskStatus.Paused
            return self.__update_task(task)
        return None
    
    def resume(self, id) -> str | None:
        task = self.get(id)
        if not task:
            return None
        if task.status == TaskStatus.Paused:
            return task.id
        self.scheduler.restore_job(task.id, task.trigger, task.func, task.args)
        return self.__update_task(task)
    
    def set_result(self, id: str, duration: timedelta = 0, result: any = None, ) -> str | None:
        task = self.get(id)
        if task:
            task.runTimes += 1
            task.lastUpdated = datetime.now()
            task.duration = duration
            task.result = result
        return self.__update_task(task)
    
    def set_trigger(self, id: str, trigger: dict) -> str | None:
        task = self.taskList.get(id, None)
        if task is None:
            return None        
        self.scheduler.reschedule_job(id, trigger)
        task.trigger = trigger
        return self.__update_task(task)

    def jobs(self) -> list:
        return self.scheduler.jobs()
    
    def __make_task_local(self, id: str) -> str:
        return f'{PATH_TASK_INSTANCE}/{id}.i'

    def __load_tasks(self, callback: callable) -> None:
        try:
            stmt = select(TaskInstanceTable)
            results = dbEngine.select(stmt)
            for result in results:
                self.__load_task(result.id, callback)
        except Exception as e:
            raise AppException(e)

    def __load_task(self, id: str, callback: callable) -> str:
        file = self.__make_task_local(id)
        with open(file, 'rb') as input:
            task = pickle.load(input)
            self.scheduler.restore_job(task.id, task.trigger, task.func, task.args)
            callback(task)
            return task.id

    def __save_task(self, task: Task) -> str:
        try:
            stmt = insert(TaskInstanceTable).values(id=task.id,type=task.type.value)
            dbEngine.insert(stmt)
            return self.__update_task(task)
        except Exception as e:
            raise AppException(e)        

    def __remove_task(self, id: str) -> str:
        try:
            stmt = delete(TaskInstanceTable).where(TaskInstanceTable.id.__eq__(id))
            dbEngine.delete(stmt)

            file = self.__make_task_local(id)
            os.remove(file)
        except Exception as e:
            raise AppException(e)
        
    def __update_task(self, task: Task) -> str:
        try:
            file = self.__make_task_local(task.id)
            with open(file, 'wb') as output:
                pickle.dump(task, output)
            return task.id
        except Exception as e:
            raise AppException(e)                


taskManager = TaskManager() 