from typing import Union, Dict, List, Any
from pydantic import BaseModel, ConfigDict

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

class RequestModel(BaseModel):
    pass

class ResponseModel(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    code: int = 0
    message: str | None = None

    # result: BaseModel | None  = None

    # def __init__(self, code: int = 0, message: str | None = None, result: BaseModel | JSONType | None = None):
    #     super().__init__(code=code, message=message, result=result)
        # self.code = 0
        # self.message = message
        # self.result = result
    # result: JSONType | None = None
