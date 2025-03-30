"""
Stock
"""
import akshare as ak
import app.database.data as common
from app.database import dbEngine


def download_history_data(code: str, start: str, end: str, period: str = 'daily', adjust: str = 'qfq') -> None:
  common.download_history_data(common.TYPE_STOCK, code, start, end, period, adjust)
  # history = ak.stock_zh_a_hist(symbol=code, period=period, adjust=adjust, start_date=start, end_date=end)
  # history = history.drop('股票代码', axis=1)
  # # table = common.make_history_data_table(common.TYPE_STOCK, code, period, adjust)
  # table = common.make_history_data_table_name(common.TYPE_STOCK, code, period, adjust)
  # history.set_index('日期', inplace=True)
  # history.to_sql(table, dbEngine.engine, if_exists='replace', index=True, index_label='日期')

  # data = history.to_dict(orient='records')
  # print(data)
  # table = common.get_history_data_table(common.TYPE_STOCK, code, period, adjust)
  # table = common.truncate_table(table)
  # dbEngine.bulk_insert_data(table, data)

  # table = fetch_table(code, datatype)
  # session = dbEngine.Session()
  # data = session.query(table).all()
  # session.close()
  # return data

def fetch_history_data(code: str, start: str, end: str, period: str = 'daily', adjust: str = 'qfq') -> list[common.HistoryData]:
  return common.fetch_history_data(common.TYPE_STOCK, code, start, end, period, adjust)
