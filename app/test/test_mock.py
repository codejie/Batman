from datetime import datetime, timedelta
import unittest
from pandas import DataFrame
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import dbEngine
from app.database.data import make_history_data_table_name
from app.exception import AppException


# def insert_download_record(type, code, period, adjust, start, end):
#   dbEngine.insert_instance(Define.DownloadRecordsTable(type=type, code=code, period=period, adjust=adjust, start=start, end=end))

def make_history_data(start: datetime, end: datetime, close: float) -> DataFrame:
  ret = DataFrame(columns=['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'])
  while start <= end:
    s = start.strftime('%Y-%m-%d')
    ret.loc[s] = [s, close, close, close, close, 0, 0, 0, 0, 0, 0]
    start = start + timedelta(days=1)

  return ret


class TestMockHistoryData(unittest.TestCase):
  def setUp(self):
    dbEngine.start()
  
  def tearDown(self):
    dbEngine.shutdown()

  def test_create_history_data(self):
    table = make_history_data_table_name(2, '100001', 'daily', 'qfq')
    self.assertTrue(table == 'stock_daily_qfq_100001')

    if not dbEngine.check_table_exist(table):
      sql = text(f"""
        CREATE TABLE IF NOT EXISTS {table} (
          "日期" DATE,
          "开盘" FLOAT, 
          "收盘" FLOAT, 
          "最高" FLOAT, 
          "最低" FLOAT, 
          "成交量" BIGINT,
          "成交额" FLOAT,
          "振幅" FLOAT,
          "涨跌幅" FLOAT,
          "涨跌额" FLOAT,
          "换手率" FLOAT
        );
        """)
      try:
        with Session(dbEngine.engine) as session:
            session.execute(sql)
            session.commit()
      except Exception as e:
        raise AppException(e)

      sql = text(f"""
          CREATE INDEX "ix_{table}_日期" ON {table} ("日期");)'
        """)
      try:
        with Session(dbEngine.engine) as session:
            session.execute(sql)
            session.commit()
      except Exception as e:
        raise AppException(e)

    self.assertTrue(True)


  def test_make_history_data(self):
    ret = make_history_data(datetime(2025, 1, 1), datetime(2025, 3, 10), 100)
    print(ret)
    self.assertTrue(True)
# def download_history_data(type: int, code: str, start: str, end: str, period: str = 'daily', adjust: str = 'qfq') -> int:
#   data = None
#   if type == Define.TYPE_STOCK:
#     data = Stock.download_history_data(code=code, period=period, adjust=adjust, start=Utils.convert_history_date_2(start), end=Utils.convert_history_date_2(end))
#   elif type == Define.TYPE_INDEX:
#     data = None

#   if data is not None:
#     table_name = make_history_data_table_name(type, code, period, adjust)
#     data.to_sql(table_name, dbEngine.engine, if_exists='replace', index=True, index_label='日期')

#     update_download_records(type, code, period, adjust, start, end)

#     return len(data)
#   else:
