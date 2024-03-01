"""
指数接口结构定义
"""
import datetime
from pydantic.fields import Field
from typing import Dict, List

from ...models import RequestModel, ResponseModel

class InfosRequest(RequestModel):
    pass

class InfosResponse(ResponseModel):
    result: Dict | None = None

class HistoryRequest(RequestModel):
    symbol: str
    start: datetime.date
    end: datetime.date
    period: str | None = Field(default="daily", description="daily/weekly/monthly")

class HistoryResponse(ResponseModel):
    result: Dict | None = None