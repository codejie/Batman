from typing import Union, Dict, List, Any
from pydantic import BaseModel

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

class RequestModel(BaseModel):
    pass

class ResponseModel(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    code: int = 0
    message: str | None = None


from . import account, data, test, toolkit

routers = data.routers + [test.router] + [account.router] + toolkit.routers