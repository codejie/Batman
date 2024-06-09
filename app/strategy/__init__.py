"""
策略基类
"""
import pickle
from enum import Enum
from app.exception import AppException
from app.strategy.algorithm import Algorithm
from app.database import dbEngine, select, delete, insert
from app.database.tables import TableBase, Column, String, Integer, DateTime, func
from app.task_scheduler import Trigger, taskScheduler

class AppStrategyException(AppException):
    def __init__(self, e: Exception) -> None:
        super().__init__(e)

    def __init__(self, message: str) -> None:
        super().__init__(message)

class Type(Enum):
    FILTER = 0,
    TRADE = 1

class Argument:
    def __init__(self, name: str, type: str, unit: str = None, desc: str = None, default: any = None, required: bool = True) -> None:
        self.name = name
        self.type = type
        self.unit = unit
        self.desc = desc
        self.default = default
        self.required = required

# class Data:
#     def __init__(self, name: str, type: str, desc: str = None) -> None:
#         self.name = name
#         self.type = type
#         self.desc = desc

class Strategy:
    type: Type
    name: str
    desc: str
    args: list[Argument] = []
    algorithms: list[Algorithm] = []
    
    def func(**kwargs) -> None:
        """
            kwargs:
                - id: instance id
                - values: strategy arg values
                - glgo_values: argorithms' args values
        """
        pass

"""
Strategy Manger
"""    
class StrategyManager:
    listStrategy: dict[str, Strategy] = {} # name + Strategy
    
    @staticmethod
    def add_strategy(strategy: Strategy) -> None:
        StrategyManager.listStrategy[strategy.name] = strategy
    
    @staticmethod
    def get_strategy(name: str) -> Strategy | None:
        return StrategyManager.listStrategy.get(name, None)
    
    @staticmethod
    def get_strategy_list(type: Type = None) -> list[Strategy]:
        ret: list = []
        for k, v in StrategyManager.listStrategy:
            if type == None or type == v.type:
                list.append(v)
        return ret
"""
Strategy Instance
"""
class State(Enum):
    INIT = 0
    READY = 1
    RUNNING = 2

class StrategyInstance:
    def __init__(self, id: str, name: str, strategy: str, trigger: Trigger) -> None:
        self.id: str = None
        self.name: str = None
        self.strategy: str = None
        self.trigger: dict = None

        self.state = State.READY
        self.arg_values: dict = None
        self.algo_values: dict[str, dict] = None

    def set_args(self, values: dict, algo_values: dict | None = None) -> None:
        for arg in self.args:
            if arg.name in values:
                self.arg_values[arg.name] = values[arg.name]
            elif not arg.required:
                self.arg_values[arg.name] = arg.default
            else:
                raise AppStrategyException(f'{self.name} missing argument {arg.name}')
        self.algo_values = algo_values # todo: check algorithm args

    def get_func() -> callable:
        pass
"""
Strategy Instance Manager
"""

PATH_STRATEGY_INSTANCE = './app/db/instance' # 'app\\db\\instance'

class StategyInstanceTable(TableBase):
    __tablename__ = 'sys_strategy_instance'

    id = Column(String, primary_key=True)
    type = Column(Integer, nullable=False)
    version = Column(String, default='1', nullable=False)
    updated = Column(DateTime(timezone=True), server_default=func.now())    

class StrategyInstanceManager:
    def __init__(self) -> None:
        self.instances: dict[str, Strategy] = {} # id + strategy instance
        self.__load_instances()

    def __load_instances(self) -> None:
        try:
            stmt = select(StategyInstanceTable)
            results = dbEngine.select(stmt)
            for result in results:
                self.__load_instance(result.id)
        except Exception as e:
            raise AppStrategyException(e)
        
    def __load_instance(self, id: str) -> str:
        file = self.__make_task_local(id)
        with open(file, 'rb') as input:
            instance = pickle.load(input)
            id = self.__schedule_instance(instance)
            self.instances[id] = instance

    def __schedule_instance(self, instance: StrategyInstance) -> str:
        strategy = StrategyManager.get_strategy(instance.strategy)
        if strategy:
            kwargs = {
                'id': instance.id,
                'values': instance.arg_values,
                'algo_values': instance.algo_values
            }
            taskScheduler.make_job(instance.id, instance.trigger, strategy.func, kwargs)
        else:
            raise AppStrategyException(f'strategy \'{instance.strategy}\' not found.')