"""
Finder Strategy Function Pipe 实例函数
"""
from datetime import datetime

class FinderStrategyInstance:
    def __init__(self, id: str, title: str, trigger: dict, strategies: list, response: dict = None) -> None:
        self.id = id
        self.title = title
        self.trigger = trigger
        self.strategies = strategies
        self.response = response
        self.runTimes = 0
        
    def set_response(self, response: dict):
        self.runTimes += 1
        self.response = response
        self.lastDate = datetime.now()

instanceList: dict[str, FinderStrategyInstance] = {}

def create(id: str, title: str, trigger: dict, strategies: list) -> bool:
    instanceList[id] = FinderStrategyInstance(id, title, trigger, strategies)
    return True

def remove(id: str) -> None:
    instanceList.pop(id, None)

def set_response(id: str, response: dict) -> None:
    instance = instanceList.get(id, None)
    if instance is not None:
        instance.set_response(response)

def get(id: str | None = None) -> dict | list[dict] | None:
    if id is None:
        return list(instanceList.values())
    else:
        return instanceList.get(id)