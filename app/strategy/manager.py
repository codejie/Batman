"""
Strategy Manager
"""
import pickle
from app.database import dbEngine, select, delete, insert
from app.database.tables import TableBase, Column, String, Integer, DateTime, func

from app.strategy import AppStrategyException, Strategy, Type
from app.task_scheduler import taskScheduler

PATH_STRATEGY_INSTANCE = './app/db/instance' # 'app\\db\\instance'

class StategyInstanceTable(TableBase):
    __tablename__ = 'sys_strategy_instance'

    id = Column(String, primary_key=True)
    type = Column(Integer, nullable=False)
    version = Column(String, default='1', nullable=False)
    updated = Column(DateTime(timezone=True), server_default=func.now())    

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
    
    def __init__(self) -> None:
        self.listInstance: dict[str, Strategy] = {} # id + strategy instance
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
            self.listInstance[id] = instance

    def __schedule_instance(self, instance: StrategyInstance) -> str:
        strategy = StrategyManager.get_strategy(instance.strategy)
        if strategy:
            kwargs = {
                'id': instance.id,
                'values': instance.arg_values
            }
            taskScheduler.make_job(instance.id, instance.trigger, strategy.func, instance.args)