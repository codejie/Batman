"""
自选股函数
"""
from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from app.routers.dependencies import verify_token
from app.routers.define import RequestModel, ResponseModel

from app.user_data import personalized

router = APIRouter(prefix='/quotes/personalized', tags=['quotes', 'personalized'], dependencies=[Depends(verify_token)])

"""
获取自选股列表
"""
class InfosRequest(RequestModel):
    code: str | None = None
    name: str | None = None
    type: int | None = None
    with_quote: bool = True
    date: str | None = None
    
class ItemQuoteResponse(BaseModel):
    date: str
    price: float
    percentage: float
    amount: float
    volatility: float
    open: float
    close: float
    high: float
    low: float
    volume: int
    turnover: float
    rate: float

    # block: int

class InfosItemResponse(BaseModel):
    id: int
    code: str
    name: str
    type: int
    comment: str | None
    quote: ItemQuoteResponse | None


class InfosResponse(ResponseModel):
    result: list[InfosItemResponse]

@router.post('/infos', response_model=InfosResponse, response_model_exclude_none=True)
async def infos(body: InfosRequest=Body()):
    result: list[InfosItemResponse] = []
    
    ret = personalized.get_list(with_quote=body.with_quote, date=body.date)
    # print(ret)
    for item in ret:
        result.append(InfosItemResponse(
            id=item['id'],
            code=item['code'],
            name=item['name'],
            type=item['type'],
            comment=item['comment'],
            quote=ItemQuoteResponse(
                date=item['quote']['date'],
                price=item['quote']['price'],
                percentage=item['quote']['percentage'],
                amount=item['quote']['amount'],
                volatility=item['quote']['volatility'],
                open=item['quote']['open'],
                close=item['quote']['close'],
                high=item['quote']['high'],
                low=item['quote']['low'],
                volume=item['quote']['volume'],
                turnover=item['quote']['turnover'],
                rate=item['quote']['rate'],
            ) if 'quote' in item else None
        ))

    return InfosResponse(result=result)

"""
添加自选股
"""
class CreateRequest(RequestModel):
    code: str | None = None
    name: str | None = None
    type: int | None = None
    comment: str | None = None

class CreateResponse(ResponseModel):
    result: int

@router.post('/create', response_model=CreateResponse, response_model_exclude_none=True)
async def create(body: CreateRequest=Body()):
    result = personalized.create(
        code=body.code,
        type=body.type,
        comment=body.comment)
    return CreateResponse(result=result)

    