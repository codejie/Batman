from fastapi import Header
from pydantic import BaseModel

DEFAULT_UID = 99

class RequestModel(BaseModel):
  pass

class ResponseModel(BaseModel):
  code: int = 0
  message: str = None

def verify_token(token: str=Header()) -> str:
    return token