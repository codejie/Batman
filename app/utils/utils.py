"""
工具集合
"""
from datetime import date, datetime, timedelta

def dateConvert1(date: str) -> str:
    """
    from 'yyyy-mm-dd' to 'yyyymmdd'
    """
    return "{}{}{}".format(date[:4],date[5:7],date[8:])

def dateConvert2(date: str) -> str:
    """
    from 'yyyymmdd' to 'yyyy-mm-dd'
    """
    return "{}-{}-{}".format(date[:4],date[4:6],date[6:])

def kwargString(kwargs):
    return ", ".join(f"{k}={v}" for k, v in kwargs.items())

def string2Date1(date: str) -> date:
    return datetime.strptime(date, '%Y%m%d').date()

def string2Date2(date: str) -> date:
    return datetime.strptime(date, '%Y-%m-%d').date()

def string2Datetime2(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

def date2String1(date: datetime.date) -> str:
    return date.strftime('%Y%m%d')

def date2String2(date: datetime.date) -> str:
    return date.strftime('%Y-%m-%d')

def datetime2String1(time: datetime) -> str:
    if time is None:
        return ''
    return time.strftime('%Y%m%d%H%M%S')

def datetime2String2(time: datetime) -> str:
    if time is None:
        return ''
    return time.strftime('%Y-%m-%d %H:%M:%S')

def timedelta2String(delta: timedelta) -> str:
    if delta is None:
        return ''
    return str(delta)

import datetime

def find_last_non_weekend_date(date=None):
    """
    找到最近一个非周末的日期

    Args:
        date (datetime.date, optional): 日期. Defaults to None.

    Returns:
        datetime.date: 最近一个非周末的日期
    """
    if date is None:
        date = datetime.date.today()
    while date.weekday() >= 5:  # 5代表星期六，6代表星期日
        date -= datetime.timedelta(days=1)
    return date