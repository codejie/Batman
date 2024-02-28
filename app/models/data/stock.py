
from typing import Dict
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
    peroid: str | None = None

class HistoryResponse(ResponseModel):
    result: Dict | None = None