"""
Strategy Manager
"""
from app.database import dbEngine, select, delete, insert
from app.database.tables import TableBase, Column, String, Integer, DateTime, func

from app.strategy import Strategy, Type
from app.task_manager import taskManager

PATH_TASK_INSTANCE = './app/db/instance' # 'app\\db\\instance'

class StategyInstanceTable(TableBase):
    __tablename__ = 'sys_strategy_instance'

    id = Column(String, primary_key=True)
    type = Column(Integer, nullable=False)
    version = Column(String, default='1', nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
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

    def load_instances(self) -> None:
