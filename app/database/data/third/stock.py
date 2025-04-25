"""
股票三方数据接口封装
"""
from pandas import DataFrame
import akshare

# from app.utils import utils
from app.database.data import utils


"""
创新高
https://data.10jqka.com.cn/rank/cxg/
- symbol
  - 0:  "创月新高"
  - 1: "半年新高"
  - 2: "一年新高"
  - 3: "历史新高"
"""

def new_high(category: int = 0) -> DataFrame:
  symbol = '创月新高' if category == 0 else '半年新高' if category == 1 else '一年新高' if category == 2 else '历史新高'
  df = akshare.stock_rank_cxg_ths(symbol=symbol)
  return df
  
"""
连续上涨
https://data.10jqka.com.cn/rank/lxsz/
"""
def uptrend(days: int = 1) -> DataFrame:
  df = akshare.stock_rank_lxsz_ths()
  if days > 1:
    df = df[df['连涨天数'] >= days]
  return df

"""
持续放量
https://data.10jqka.com.cn/rank/cxfl/
"""
def high_volume(days: int = 1) -> DataFrame:
  df = akshare.stock_rank_cxfl_ths()
  if days > 1:
    df = df[df['放量天数'] >= days]
  return df

"""
量价齐升
https://data.10jqka.com.cn/rank/ljqs/
"""
def rise_volume_price(days: int = 1) -> DataFrame:
  df = akshare.stock_rank_ljqs_ths()
  if days > 1:
    df = df[df['量价齐升天数'] >= days]
  return df

"""
涨停股池
https://quote.eastmoney.com/ztb/detail#type=ztgc
"""
def limit_up_pool(date: str = None) -> DataFrame:
  if date is None:
    date = utils.date_to_string_2(utils.get_latest_workday())
  df = akshare.stock_zt_pool_em(date=date)
  return df
