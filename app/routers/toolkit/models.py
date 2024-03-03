"""
工具类接口结构定义
"""
from typing import Dict, List
from pydantic.fields import Field

from .. import RequestModel, ResponseModel

"""
TA分析接口接口定义
"""
class MARequest(RequestModel):
    ds: Dict = Field(description='数据集合')
    columns: List[str] | None = Field(default=None, description='需要处理的数据集合列名')
    periods: List[int] | None = Field(default=[5], description='MA分析周期，支持多个周期')
    types: List[str] | None = Field(default=['SMA'], description='MA类型：SMA/EMA/WMA/DEMA/TEMA/TRIMA/KAMA/MAMA/T3')

class MAResponse(ResponseModel):
    result: Dict | None = Field(default=None, description='结果集合，列名格式为：{col}_{type}{period}')

class BBANDSRequest(RequestModel):
    ds: Dict = Field(description='数据集合')
    columns: List[str] | None = Field(default=None, description='需要处理的数据集合列名')
    period: int | None = Field(default=5, description='分析周期')
    upper: int | None = Field(default=2, description='上轨线标准差倍数')
    lower: int | None = Field(default=2, description='下轨线标准差倍数')
    types: List[str] | None = Field(default=['SMA'], description='MA类型：SMA/EMA/WMA/DEMA/TEMA/TRIMA/KAMA/MAMA/T3')

class BBANDSResponse(ResponseModel):
    result: Dict | None = Field(default=None, description='结果集合，包括上轨数据{col}_upper、中轨数据{col}_middle、下柜数据{col}_lower')