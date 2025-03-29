"""
Stock
"""
import akshare as ak
import app.database.data as common
from app.database import dbEngine


def download_history_data(code: str, start: str, end: str, period: str = 'daily', adjust: str = 'qfq') -> None:
  history = ak.stock_zh_a_hist(symbol=code, period=period, adjust=adjust, start_date=start, end_date=end)
  history = history.drop('股票代码', axis=1)
  data = history.to_dict(orient='records')
  print(data)
  table = common.get_history_data_table(common.TYPE_STOCK, code, period, adjust)
  for record in data:
      
  table = common.truncate_table(table)
  dbEngine.bulk_insert_data(table, data)
  # table = fetch_table(code, datatype)
  # session = dbEngine.Session()
  # data = session.query(table).all()
  # session.close()
  # return data