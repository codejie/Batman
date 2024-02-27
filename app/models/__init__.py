from typing import Union, Dict, List, Any
from pydantic import BaseModel

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

class Request(BaseModel):
    pass

class Response(BaseModel):
    code: int = 0
    message: str | None = None
    result: JSONType | None = None
