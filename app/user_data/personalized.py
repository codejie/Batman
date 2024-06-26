"""
自选股函数
"""
from sqlalchemy import select,delete
from sqlalchemy.orm import Session
from app.dbengine import engine
from app.user_data import PersonalizedTable

from app import AppException
from app.data import DataType, StockAListTable
from app.user_data import common_stock as CommonStock
from app import utils

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
                'updated': utils.date2String2(item.updated)
            })

    with_quote = kwargs['with_quote']
    if with_quote:
        date = kwargs['date'] if 'date' in kwargs else None
        for item in ret:
            df = CommonStock.get_daily_history_quote(code=item['code'], date=date)
            if not df.empty:
                item['quote'] = {
                    'date': df['日期'][0],
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

    stmt = select(PersonalizedTable).where(PersonalizedTable.code == code)
    with Session(engine) as session:
        exist = session.query(PersonalizedTable.id).filter_by(code=code).first() is not None
        if exist:
            raise AppException(f'{code} exist')

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

"""
remove
"""
def remove(**kwargs) -> int:
    id = kwargs['id']
    if type(id) is int:
        id = [id]
    stmt = delete(PersonalizedTable).where(PersonalizedTable.id.in_(id))
    with Session(engine) as session:
        result = session.execute(stmt)
        session.commit()

        return result.rowcount
