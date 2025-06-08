
import random
from typing import Optional
from app.database.data.define import SpotData


def generate_random_spot_data() -> SpotData:
    # 生成随机字符串
    def random_string(length: int) -> str:
        return '000001'

    # 随机决定 Optional 字段是否赋值
    def random_optional_float(min_val: float, max_val: float) -> float:
        return round(random.uniform(min_val, max_val), 2) # if random.choice([True, False]) else None

    # 生成随机数据
    latest_price = round(random.uniform(1.0, 1000.0), 2)  # 最新价
    yesterday_close = round(random.uniform(1.0, 1000.0), 2)  # 昨收
    change_amount = round(latest_price - yesterday_close, 2)  # 涨跌额
    change_percent = round((change_amount / yesterday_close) * 100, 2)  # 涨跌幅

    return SpotData(
        序号=random.randint(1, 10000),  # 随机序号
        代码=random_string(6),  # 随机6位代码
        名称=random_string(4),  # 随机4位名称
        最新价=latest_price,
        涨跌幅=change_percent,
        涨跌额=change_amount,
        成交量=round(random.uniform(1000.0, 1000000.0), 2),  # 随机成交量
        成交额=round(random.uniform(100000.0, 100000000.0), 2),  # 随机成交额
        振幅=round(random.uniform(0.0, 10.0), 2),  # 随机振幅
        最高=round(random.uniform(latest_price, latest_price + 50.0), 2),  # 最高价
        最低=round(random.uniform(max(0.1, latest_price - 50.0), latest_price), 2),  # 最低价
        今开=round(random.uniform(max(0.1, latest_price - 20.0), latest_price + 20.0), 2),  # 今开
        昨收=yesterday_close,
        量比=round(random.uniform(0.1, 5.0), 2),  # 随机量比
        换手率=random_optional_float(0.0, 20.0),  # 随机换手率
        市盈率=random_optional_float(-50.0, 100.0),  # 随机市盈率
        市净率=random_optional_float(0.5, 10.0),  # 随机市净率
        总市值=random_optional_float(100000000.0, 10000000000.0),  # 随机总市值
        流通市值=random_optional_float(50000000.0, 5000000000.0),  # 随机流通市值
        涨速=random_optional_float(-5.0, 5.0),  # 随机涨速
        涨跌5分钟=random_optional_float(-2.0, 2.0),  # 随机5分钟涨跌
        涨跌幅60日=random_optional_float(-30.0, 30.0),  # 随机60日涨跌幅
        年初至今涨跌幅=random_optional_float(-50.0, 50.0),  # 随机年初至今涨跌幅
    )