
from typing import Dict, List
from pydantic.fields import Field
import datetime

from ...models import RequestModel, ResponseModel

class IndividualInfoRequest(RequestModel):
    symbol: str

class IndividualInfoResponse(ResponseModel):
    result: Dict | None = None

class HistoryRequest(RequestModel):
    symbol: str
    start: datetime.date
    end: datetime.date
    period: str | None = Field(default="daily", description="daily/weekly/monthly")

class HistoryResponse(ResponseModel):
    result: Dict | None = None

class SpotRequest(RequestModel):
    symbols: List[str] | None = None

class SpotResponse(ResponseModel):
    result: Dict | None = None