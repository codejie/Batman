
"""
内容记录
"""

class FinderStrategyInstance:
    def __init__(self, id: str, name: str, strategy: str, args: dict | None, response: dict = None) -> None:
        self._id = id
        self._name = name
        self._strategy = strategy
        self._args = args
        self._response = response
        
    def setResponse(self, response: dict):
        self._response = response

"""
FinderStrategyInstanceList in local cache
""" 

finderStrategyInstanceList: dict[str, FinderStrategyInstance] = {}

def createFinderStrategyInstance(id: str, name: str, strategy: str, args: dict = None) -> bool:
    finderStrategyInstanceList[id] = FinderStrategyInstance(id, name, strategy, args)
    return True

def removeFinderStrategyInstance(id: str) -> None:
    finderStrategyInstanceList.pop(id, None)

def setFinderStrategyInstanceResponse(id: str, response: dict) -> None:
    finderStrategyInstanceList[id].setResponse(response)

def getFinderStrategyInstance(id: str | None = None) -> dict | list[dict] | None:
    if id is None:
        return finderStrategyInstanceList.values()
    else:
        return finderStrategyInstanceList.get(id)
