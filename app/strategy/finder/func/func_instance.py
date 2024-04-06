from datetime import datetime
"""
Finder Strategy Function 实例函数
"""

class FinderStrategyInstance:
    def __init__(self, id: str, title: str, trigger: dict, strategy: str, args: dict | None, response: dict = None) -> None:
        self.id = id
        self.title = title
        self.trigger = trigger
        self.strategy = strategy
        self.args = args
        self.runTimes = 0
        # self.endDate = None
        self.response = response
        
    def set_response(self, response: dict):
        self.runTimes += 1
        self.lastDate = datetime.now()
        self.response = response

"""
FinderStrategyInstanceList in local cache
""" 

instanceList: dict[str, FinderStrategyInstance] = {}

def create(id: str, title: str, trigger: dict, strategy: str, args: dict = None) -> bool:
    instanceList[id] = FinderStrategyInstance(id, title, trigger, strategy, args)
    return True

def remove(id: str) -> None:
    instanceList.pop(id, None)

def set_response(id: str, response: dict) -> None:
    instance = instanceList.get(id, None)
    if instance is not None:
        instance.set_response(response)

def get(id: str | None = None, strategy: str | None = None) -> dict | list[dict] | None:
    if id is None and strategy is None:
        return list(instanceList.values())
    elif id is None:
        ret = []
        for k, v in instanceList.items():
            if v.strategy == strategy:
                ret.append(v)
        return ret
    else:
        return instanceList.get(id)

def set_trigger(id: str, trigger: dict) -> None:
    instance = instanceList.get(id, None)
    if instance is not None:
        instance.trigger = trigger