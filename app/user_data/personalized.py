"""
自选股函数
"""
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dbengine import engine
from app.user_data import PersonalizedTable

from app import AppException
from app.data import DataType, StockAListTable
from app.user_data import common_stock as CommonStock
from app.data import stock

def get_list(**kwargs) -> list:
    ret = []
    stmt = select(PersonalizedTable)
    with Session(engine) as session:
        for item in session.scalars(stmt):
            ret.append({
                'id': item.id,
                'code': item.code,
                'name': item.name,
                'type': item.type,
                'comment': item.comment,
                'updated': item.updated
            })

    with_quote = kwargs['with_quote']
    if with_quote:
        date = kwargs['date']
        for item in ret:
            df = CommonStock.get_daily_history_quote(code=item['code'], date=date)
            if not df.empty:
                item['quote'] = {
                    'price': df['收盘'][0],
                    'percentage': df['涨跌幅'][0],
                    'amount': df['涨跌额'][0],
                    'volatility': df['振幅'][0],
                    'open': df['开盘'][0],
                    'close': df['收盘'][0],
                    'high': df['最高'][0],
                    'low': df['最低'][0],
                    'volume': df['成交量'][0],
                    'turnover': df['成交额'][0],
                    'rate': df['换手率'][0],
                }

    return ret

def create(**kwargs) -> int:
    # print(kwargs)
    code=kwargs['code']
    comment=kwargs['comment'] if 'comment' in kwargs and kwargs['comment'] else None
    type = int(kwargs['type']) if 'type' in kwargs and kwargs['type'] else DataType.STOCK.value

    stmt = select(StockAListTable).where(StockAListTable.code.__eq__(code))
    with Session(engine) as session:
        ret = session.scalars(stmt).one_or_none()
        if ret:
            session.add(PersonalizedTable(
                code=code,
                name=ret.name,
                type=type,
                comment=comment
            ))
            session.commit()
            return 0
        else:
            raise AppException(f'{code} not found')
