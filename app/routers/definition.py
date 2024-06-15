
from pydantic import BaseModel, ConfigDict
from fastapi import Header, HTTPException, APIRouter, Depends, Body

class RequestModel(BaseModel):
    pass

class ResponseModel(BaseModel):
    code: int = 0
    message: str = None

def verify_token(token: str=Header()) -> str:
    return token

def verify_admin_token(token: str=Header()) -> str:
    if token != 'superman':
        raise HTTPException(status_code=400, detail="Token invalid.")    
    return token