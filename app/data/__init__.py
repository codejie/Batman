"""
数据定义
"""

from enum import Enum

from datetime import datetime
from typing import Optional
from sqlalchemy.sql import func
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.dbengine import Base

class DataType(Enum):
    STOCK = 1
    INDEX = 1000

"""
数据表结构定义
"""
class StockAListTable(Base):
    __tablename__ = 'stock_a_list'

    code: Mapped[str] = mapped_column(String(6), primary_key=True)
    name: Mapped[str] = mapped_column(String(16))