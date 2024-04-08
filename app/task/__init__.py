"""
系统任务管理
"""
from enum import Enum
from datetime import datetime, timedelta

class TaskType(Enum):
    All = 0
    FinderStrategyInstance = 1
    PipeFinderStrategyInstance = 2
    SysDataInstance = 3
    SysWatchInstance = 4

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

    def create(self, type: TaskType, id: str, trigger: dict, element: dict) -> bool:
        self.taskList[id] = Task(type, id, trigger, element)
        return True
    
    def remove(self, id) -> None:
        self.taskList.pop(id, None)

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

    # def set_element_arg(self, id, arg: str, value: any) -> str | None:
    #     task = self.taskList.get(id, None)
    #     if task is None:
    #         return None
    #     task.element[arg] = value
    #     return id

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
        task.trigger = trigger
        return id

    def create_finder_strategy(self, id: str, title: str, trigger: dict, strategy: str, args: dict = None) -> bool:
        return self.create(TaskType.FinderStrategyInstance, id, trigger, {
            'title': title,
            'strategy': strategy,
            'args': args,
        })
    
    def create_pipe_finder_strategy(self, id: str, title: str, trigger: dict, strategies: list) -> bool:
        return self.create(TaskType.PipeFinderStrategyInstance, id, trigger, {
            'title': title,
            'strategies': strategies
        })

taskManager = TaskManager() 