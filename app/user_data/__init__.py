"""
用户数据
"""
from datetime import datetime
from typing import Optional
from sqlalchemy.sql import func
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.dbengine import Base
"""
用户表
"""
class PersonalizedTable(Base):
    __tablename__ = 'user_personalized'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    code: Mapped[str] = mapped_column(String(6), unique=True)
    name: Mapped[str] = mapped_column(String(16))
    type: Mapped[int] = mapped_column(default=1)
    comment: Mapped[Optional[str]]
    updated: Mapped[datetime] = mapped_column(server_default=func.now())
    
    # price: Mapped[float]
    # percentage: Mapped[float]
    # amount: Mapped[float]
    # volatility: Mapped[float]
    # open: Mapped[float]
    # close: Mapped[float]
    # high: Mapped[float]
    # low: Mapped[float]
    # volume: Mapped[int]
    # turnover: Mapped[float]
    # rate: Mapped[float]

    def __repr__(self) -> str:
        return f'Personalized(code={self.code!r}, name={self.name!r})'