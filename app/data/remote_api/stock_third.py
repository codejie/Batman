"""
股票三方数据接口封装
"""
from pandas import DataFrame
import akshare


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
  print(df)
  return df
  
