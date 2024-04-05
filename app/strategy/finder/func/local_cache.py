from datetime import datetime
"""
内容记录
"""

class FinderStrategyInstance:
    def __init__(self, id: str, title: str, trigger: dict, strategy: str, args: dict | None, response: dict = None) -> None:
        self.id = id
        self.title = title
        self.trigger = trigger
        self.strategy = strategy
        self.args = args
        self.runTimes = 0
        self.endDate = None
        self.response = response
        
    def setResponse(self, response: dict):
        self.runTimes += 1
        self.runDate = datetime.now()
        self.response = response

"""
FinderStrategyInstanceList in local cache
""" 

finderStrategyInstanceList: dict[str, FinderStrategyInstance] = {}

def createFinderStrategyInstance(id: str, title: str, trigger: dict, strategy: str, args: dict = None) -> bool:
    finderStrategyInstanceList[id] = FinderStrategyInstance(id, title, trigger, strategy, args)
    return True

def removeFinderStrategyInstance(id: str) -> None:
    finderStrategyInstanceList.pop(id, None)

def setFinderStrategyInstanceResponse(id: str, response: dict) -> None:
    instance = finderStrategyInstanceList.get(id, None)
    if instance is not None:
        instance.setResponse(response)
        instance.endDate = datetime.now().strftime('%Y%m%d %H:%M:%S')

def getFinderStrategyInstance(id: str | None = None, strategy: str | None = None) -> dict | list[dict] | None:
    if id is None and strategy is None:
        return list(finderStrategyInstanceList.values())
    elif id is None:
        ret = []
        for k, v in finderStrategyInstanceList.items():
            if v.strategy == strategy:
                ret.append(v)
        return ret
    else:
        return finderStrategyInstanceList.get(id)
