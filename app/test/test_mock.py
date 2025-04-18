import unittest
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import dbEngine
from app.database.data import make_history_data_table_name
from app.exception import AppException

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
        raise Exception(e)

      sql = text(f"""
          CREATE INDEX "ix_{table}_日期" ON {table} ("日期");)'
        """)
      try:
        with Session(dbEngine.engine) as session:
            session.execute(sql)
            session.commit()
      except Exception as e:
        raise Exception(e)

    self.assertTrue(True)