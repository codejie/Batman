from datetime import datetime, timedelta
import unittest
from pandas import DataFrame
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import dbEngine
from app.database.data import make_history_data_table_name, update_download_records
from app.exception import AppException

# def insert_download_record(type, code, period, adjust, start, end):
#   dbEngine.insert_instance(Define.DownloadRecordsTable(type=type, code=code, period=period, adjust=adjust, start=start, end=end))

def make_history_data(start: datetime, end: datetime, close: float) -> DataFrame:
  ret = DataFrame(columns=['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'], index=['日期'])
  while start <= end:
    if start.weekday() < 5:
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
    ret = make_history_data(datetime(2025, 1, 1), datetime(2025, 5, 10), 1)
    print(ret)

    table = make_history_data_table_name(2, '100001', 'daily', 'qfq')
    self.assertTrue(table == 'stock_daily_qfq_100001')

    ret.to_sql(table, dbEngine.engine, if_exists='replace', index=False, index_label='日期')
    update_download_records(2, '100001', 'daily', 'qfq', '2025-01-01', '2025-03-10')

    self.assertTrue(True)

