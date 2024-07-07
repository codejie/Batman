
"""
Strategy Manger
"""

from datetime import datetime
import os
import pickle
from app.database import dbEngine, select, delete, insert, update
from app.database.tables import TableBase, Column, String, Integer, DateTime, func
from app.exception import AppException
from app.task_scheduler import taskScheduler #, EVENT_JOB_REMOVED, EVENT_JOB_ADDED, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED
from apscheduler.events import EVENT_JOB_REMOVED, EVENT_JOB_ADDED, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED
from app.database.tables import TableBase
from app.strategy import AppException, Strategy, StrategyInstance, Type, State

from app.strategy.filter.rapid_raise_fall import RapidRaiseFallStrategy


class StrategyManager:
    listStrategy: dict[str, Strategy] = {} # id + Strategy
    
    @staticmethod
    def add(strategy: Strategy) -> None:
        StrategyManager.listStrategy[strategy.id] = strategy
    
    @staticmethod
    def get(id: str) -> Strategy | None:
        return StrategyManager.listStrategy.get(id, None)
    
    @staticmethod
    def get_list(type: Type = None) -> list[Strategy]:
        ret: list = []
        for k, v in StrategyManager.listStrategy.items():
            if type == None or type == v.type:
                ret.append(v)
        return ret
    
StrategyManager.add(RapidRaiseFallStrategy)
    
"""
Strategy Instance Manager
"""

PATH_STRATEGY_INSTANCE = './app/db/instance' # 'app\\db\\instance'
# PATH_STRATEGY_INSTANCE = 'app\\db\\instance'

class StategyInstanceTable(TableBase):
    __tablename__ = 'sys_strategy_instance'

    id = Column(String, primary_key=True)
    # type = Column(Integer, nullable=False)
    version = Column(String, default='1', nullable=False)
    updated = Column(DateTime(timezone=True), server_default=func.now())    

class StrategyInstanceManager:
    def __init__(self) -> None:
        self.instances: dict[str, StrategyInstance] = {} # id + strategy instance
        taskScheduler.register_listener(self.__on_scheduler_event)

    def __on_scheduler_event(self, event: int, id: str) -> None:
        instance = self.instances.get(id, None)
        if not instance:
            return None
        if event == EVENT_JOB_ADDED:
            instance.set_state(State.READY)
        elif event == EVENT_JOB_EXECUTED:
            instance.set_state(State.EXECUTED)
        elif event == EVENT_JOB_ERROR:
            instance.set_state(State.ERROR)
        elif event == EVENT_JOB_MISSED:
            instance.set_state(State.MISSED)
        elif event == EVENT_JOB_REMOVED:
            instance.set_state(State.REMOVED)
            instance.set_removed(True)
        else:
            pass

    def __load_instances(self) -> None:
        try:
            stmt = select(StategyInstanceTable)
            results = dbEngine.select(stmt)
            for result in results:
                self.__load(result.id)
        except Exception as e:
            raise AppException(e)
        
    def __make_local_file(self, id: str) -> str:
        return f'{PATH_STRATEGY_INSTANCE}/{id}.i'
         
    def __load(self, id: str) -> str:
        file = self.__make_local_file(id)
        with open(file, 'rb') as input:
            instance = pickle.load(input)
            if not instance.is_removed:
                self.__schedule(instance)
            self.instances[id] = instance

    def __schedule(self, instance: StrategyInstance) -> str:
        strategy = StrategyManager.get(instance.strategy)
        if strategy:
            kwargs = {
                'manager': self,
                'id': instance.id,
                'values': instance.arg_values,
                'algo_values': instance.algo_values
            }

            return taskScheduler.make_job(instance.id, instance.trigger, strategy.func, kwargs)
        else:
            raise AppException(f'strategy \'{instance.strategy}\' not found.')
        
    def __save(self, instance: StrategyInstance) -> str:
        file = self.__make_local_file(instance.id)
        with open(file, 'wb') as output:
            pickle.dump(instance, output)

        stmt = insert(StategyInstanceTable).values(id=instance.id)
        dbEngine.insert(stmt)

        return instance.id
        
    def __update(self, instance: StrategyInstance) -> str:
        file = self.__make_local_file(instance.id)
        with open(file, 'wb') as output:
            pickle.dump(instance, output)

        stmt = update(StategyInstanceTable).where(StategyInstanceTable.id.__eq__(instance.id)).values(updated=func.now())
        dbEngine.update(stmt)
                    
        return instance.id
    
    def __remove(self, id: str) -> str:
        stmt = delete(StategyInstanceTable).where(StategyInstanceTable.id.__eq__(id))
        dbEngine.delete(stmt)

        file = self.__make_local_file(id)
        os.remove(file)
        return id
    
    def start(self) -> None:
        self.__load_instances()

    def shutdown(self) -> None:
        pass
    
    def get(self, id: str) -> StrategyInstance:
        instance = self.instances.get(id, None)
        if instance:
            return instance
        else:
            raise AppException(f'instance \'{id}\' not found.')
        
    def list(self, strategy: str = None, type: Type = None) -> list[StrategyInstance]:
        if strategy:
            ret = []
            for i in self.instances.values():
                if i.strategy == strategy:
                    ret.append(i)
            return ret
        elif type:
            ret = []
            for i in self.instances.values():
                if i.type == type:
                    ret.append(i)
            return ret            
        else:
            return list(self.instances.values())
    
    def add(self, name: str, strategy: str, trigger: dict, values: dict, algo_values: dict | None = None) -> str:
        stgy = StrategyManager.get(strategy)
        if not stgy:
            raise AppException(f'strategy \'{strategy}\' not found.')

        try:
            id = taskScheduler.make_id()
            instance = StrategyInstance(stgy.type, id, name, strategy, trigger)
            instance.set_args(stgy, values, algo_values)
            
            self.__schedule(instance)
            self.__save(instance)
            self.instances[id] = instance

            return instance.id
        except Exception as e:
            raise AppException(e)
        
    def remove(self, id: str) -> str:
        try:
            instance = self.instances.pop(id)
            self.__remove(id)  
            if instance and not instance.is_removed:
                taskScheduler.remove_job(id)
            return instance.id
        except Exception as e:
            raise AppException(e)

    def set_trigger(self, id: str, trigger: dict) -> str:
        try:
            taskScheduler.reschedule_job(id, trigger)

            instance = self.get(id)
            instance.set_trigger(trigger)            
            
            return self.__update(instance)
        except Exception as e:
            raise AppException(e)

    def set_args(self, id: str, values: dict, algo_values: dict | None = None) -> str:
        try:
            instance = self.get(id)
            instance.set_args(values, algo_values)            
            
            return self.__update(instance)
        except Exception as e:
            raise AppException(e)
        
    def set_results(self, id: str, results: list) -> str:
        try:
            instance = self.get(id)
            instance.results = results
            instance.latest_updated = datetime.now()    
            
            return self.__update(instance)
        except Exception as e:
            raise AppException(e)

strategyInstanceManager = StrategyInstanceManager() 