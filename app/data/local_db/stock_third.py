"""
股票三方数据入库接口封装
"""

"""
创新高
"""
from app.data.remote_api import stock_third
from app.database import dbEngine
from app.database.stock_third import TableName
from app.utils import utils


def download_new_high() -> None:
  # monthly
  df = stock_third.new_high(0)
  if not df.empty:
    df.to_sql(TableName.New_High_0, dbEngine.get_engine(), if_exists='replace', index=False)
  # half year
  df = stock_third.new_high(1)
  if not df.empty:
    df.to_sql(TableName.New_High_1, dbEngine.get_engine(), if_exists='replace', index=False)
  # year
  df = stock_third.new_high(2)
  if not df.empty:
    df.to_sql(TableName.New_High_2, dbEngine.get_engine(), if_exists='replace', index=False)
  # history
  df = stock_third.new_high(3)
  if not df.empty:
    df.to_sql(TableName.New_High_3, dbEngine.get_engine(), if_exists='replace', index=False)

def download_uptrend() -> None:
  df = stock_third.uptrend()
  if not df.empty:
    df.to_sql(TableName.Uptrend, dbEngine.get_engine(), if_exists='replace', index=False)

def download_high_volume() -> None:
  df = stock_third.high_volume()
  if not df.empty:
    df.to_sql(TableName.High_Volume, dbEngine.get_engine(), if_exists='replace', index=False)

def download_rise_volume_price() -> None:
  df = stock_third.rise_volume_price()
  if not df.empty:
    df.to_sql(TableName.Rise_Volume_Price, dbEngine.get_engine(), if_exists='replace', index=False)

def download_limit_up_pool() -> None:
  date = utils.date2String1(utils.find_last_non_weekend_date())
  df = stock_third.limit_up_pool(date=date)
  if not df.empty:
    df.to_sql(TableName.Limit_Up_Pool, dbEngine.get_engine(), if_exists='replace', index=False)