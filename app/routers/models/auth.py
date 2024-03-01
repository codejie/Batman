from pydantic import BaseModel
from datetime import datetime
from . import RequestModel, ResponseModel

class LoginRequest(RequestModel):
    account: int
    passwd: str

class LoginResult(BaseModel):
    token: str
    expired: datetime | None = None


class LoginResponse(ResponseModel):
    result: LoginResult | None = None