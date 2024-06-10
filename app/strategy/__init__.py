"""
策略基类
"""
# import os
# import pickle
from enum import Enum
from app.exception import AppException
from app.strategy.algorithm import Algorithm
# from app.database import dbEngine, select, delete, insert, update
# from app.database.tables import TableBase, Column, String, Integer, DateTime, func
# from app.task_scheduler import taskScheduler

class AppStrategyException(AppException):
    def __init__(self, e: Exception) -> None:
        super().__init__(e)

    def __init__(self, message: str) -> None:
        super().__init__(message)

class Type(Enum):
    FILTER = 0,
    TRADE = 1

class Argument:
    def __init__(self, name: str, type: str, unit: str = None, desc: str = None, values:list[tuple[any, str]] = None, default: any = None, required: bool = True) -> None:
        self.name = name
        self.type = type
        self.unit = unit
        self.desc = desc
        self.value = values
        self.default = default
        self.required = required
    
class Result:
    def __init__(self, name: str, type: str, desc: str = None) -> None:
        self.name = name
        self.type = type
        self.desc = desc    

# class Data:
#     def __init__(self, name: str, type: str, desc: str = None) -> None:
#         self.name = name
#         self.type = type
#         self.desc = desc

class Strategy:
    id: str
    type: Type
    name: str
    desc: str
    args: list[Argument] = None
    algorithms: list[Algorithm] = None
    results: list[Result] = None
    
    @staticmethod
    def func(**kwargs) -> None:
        """
            kwargs:
                - id: instance id
                - values: strategy arg values
                - algo_values: argorithms' args values
        """
        pass

# """
# Strategy Manger
# """    
# class StrategyManager:
#     listStrategy: dict[str, Strategy] = {} # id + Strategy
    
#     @staticmethod
#     def add(strategy: Strategy) -> None:
#         StrategyManager.listStrategy[strategy.id] = strategy
    
#     @staticmethod
#     def get(id: str) -> Strategy | None:
#         return StrategyManager.listStrategy.get(id, None)
    
#     @staticmethod
#     def get_list(type: Type = None) -> list[Strategy]:
#         ret: list = []
#         for k, v in StrategyManager.listStrategy:
#             if type == None or type == v.type:
#                 list.append(v)
#         return ret
"""
Strategy Instance
"""
class State(Enum):
    INIT = 0
    READY = 1
    RUNNING = 2
    PAUSED = 3

class StrategyInstance:
    def __init__(self, id: str, name: str, strategy: str, trigger: dict) -> None:
        self.id: str = None
        self.name: str = None
        self.strategy: str = None # strategy.id
        self.trigger: dict = None

        self.state = State.READY
        self.arg_values: dict = {}
        self.algo_values: dict[str, dict] = {}

    def set_args(self, strategy: Strategy, values: dict, algo_values: dict[str, dict] | None = None) -> None:
        # strategy = StrategyManager.get(self.strategy)
        # if not strategy:
        #     raise AppStrategyException(f'{self.name} strategy \'{self.strategy}\' not found.')
        
        args = strategy.args
        for arg in args:
            if arg.name in values:
                self.arg_values[arg.name] = values[arg.name]
            elif not arg.required:
                self.arg_values[arg.name] = arg.default
            else:
                raise AppStrategyException(f'{self.name} missing argument {arg.name}')
        self.algo_values = algo_values # todo: check algorithm args

    def set_trigger(self, trigger:dict) -> None:
        self.trigger = trigger

    def set_state(self, state: State) -> None:
        self.state = state

    def get_func() -> callable:
        pass
# """
# Strategy Instance Manager
# """

# PATH_STRATEGY_INSTANCE = './app/db/instance' # 'app\\db\\instance'

# class StategyInstanceTable(TableBase):
#     __tablename__ = 'sys_strategy_instance'

#     id = Column(String, primary_key=True)
#     # type = Column(Integer, nullable=False)
#     version = Column(String, default='1', nullable=False)
#     updated = Column(DateTime(timezone=True), server_default=func.now())    

# class StrategyInstanceManager:
#     def __init__(self) -> None:
#         self.instances: dict[str, StrategyInstance] = {} # id + strategy instance

#     def __load_instances(self) -> None:
#         try:
#             stmt = select(StategyInstanceTable)
#             results = dbEngine.select(stmt)
#             for result in results:
#                 self.__load(result.id)
#         except Exception as e:
#             raise AppStrategyException(e)
        
#     def __make_local_file(self, id: str) -> str:
#         return f'{PATH_STRATEGY_INSTANCE}/{id}.i'
         
#     def __load(self, id: str) -> str:
#         file = self.__make_local_file(id)
#         with open(file, 'rb') as input:
#             instance = pickle.load(input)
#             id = self.__schedule(instance)
#             self.instances[id] = instance

#     def __schedule(self, instance: StrategyInstance) -> str:
#         strategy = StrategyManager.get(instance.strategy)
#         if strategy:
#             kwargs = {
#                 'id': instance.id,
#                 'values': instance.arg_values,
#                 'algo_values': instance.algo_values
#             }

#             return taskScheduler.make_job(instance.id, instance.trigger, strategy.func, kwargs)
#         else:
#             raise AppStrategyException(f'strategy \'{instance.strategy}\' not found.')
        
#     def __save(self, instance: StrategyInstance) -> str:
#         stmt = insert(StategyInstanceTable).values(id=instance.id)
#         dbEngine.insert(stmt)

#         file = self.__make_local_file(instance.id)
#         with open(file, 'wb') as output:
#             pickle.dump(instance, output)
#         return instance.id
        
#     def __update(self, instance: StrategyInstance) -> str:
#         stmt = update(StategyInstanceTable).where(StategyInstanceTable.id.__eq__(instance.id)).values(updated=func.now())
#         dbEngine.update(stmt)
        
#         file = self.__make_local_file(instance.id)
#         with open(file, 'wb') as output:
#             pickle.dump(instance, output)
#         return instance.id
    
#     def __remove(self, id: str) -> str:
#         stmt = delete(StategyInstanceTable).where(StategyInstanceTable.id.__eq__(id))
#         dbEngine.delete(stmt)

#         file = self.__make_local_file(id)
#         os.remove(file)
#         return id
    
#     def start(self) -> None:
#         self.__load_instances()

#     def shutdown(self) -> None:
#         pass
    
#     def get(self, id: str) -> StrategyInstance:
#         instance = self.instances.get(id, None)
#         if instance:
#             return instance
#         else:
#             raise AppStrategyException(f'instance \'{id}\' not found.')
        
#     def list(self) -> list[StrategyInstance]:
#         return list(self.instances.values())
    
#     def add(self, name: str, strategy: str, trigger: dict, values: dict, algo_values: dict | None = None) -> str:
#         try:
#             id = taskScheduler.make_id()
#             instance = StrategyInstance(id, name, strategy, trigger)
#             instance.set_args(values, algo_values)
            
#             self.__schedule(instance)
#             self.__save(instance)
#             self.instances[id] = instance

#             return instance.id
#         except Exception as e:
#             raise AppStrategyException(e)
        
#     def remove(self, id: str) -> str:
#         try:
#             taskScheduler.remove_job(id)
#             self.__remove(id)            
#             instance = self.instances.pop(id)
#             return instance.id
#         except Exception as e:
#             raise AppStrategyException(e)

#     def set_trigger(self, id: str, trigger: dict) -> str:
#         try:
#             taskScheduler.reschedule_job(id, trigger)

#             instance = self.get(id)
#             instance.set_trigger(trigger)            
            
#             return self.__update(instance)
#         except Exception as e:
#             raise AppStrategyException(e)

#     def set_args(self, id: str, values: dict, algo_values: dict | None = None) -> str:
#         try:
#             instance = self.get(id)
#             instance.set_args(values, algo_values)            
            
#             return self.__update(instance)
#         except Exception as e:
#             raise AppStrategyException(e)

# strategyInstanceManager = StrategyInstanceManager()