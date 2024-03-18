"""
Finder Strategy APIs
"""

from fastapi import APIRouter, Depends, Body

from ...main import scheduler
from ..dependencies import verify_token

router = APIRouter(prefix='/strategy/finder', tag=['strategy', 'finder strategy'], dependencies=[Depends(verify_token)])

"""
获取Finder策略列表
"""
