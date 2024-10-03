
from app.data.local_db import stock_third as local

def update_daily(**kwargs) -> None:
  local.download_new_high()
  local.download_uptrend()
  local.download_high_volume()
  local.download_rise_volume_price()
  local.download_limit_up_pool()