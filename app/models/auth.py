from . import Request, Response

class LoginRequest(Request):
    account: int
    passwd: str

class LoginResponse(Response):
    result: 
    token: str | None = None