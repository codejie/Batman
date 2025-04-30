import unittest
import zipfile
from sqlalchemy import select
from app.database import dbEngine, holding
from app.database import holding as HoldingTable
from app.database.data import index as Index, stock as Stock

class TestUserHoldingTable(unittest.TestCase):
  def setUp(self):
    # Setup code to initialize the database connection and UserHoldingTable instance
    dbEngine.start()

  def tearDown(self):
    dbEngine.shutdown()

  def test_insert_record(self):
    # Test data
    record = {
      'user_id': 1
    }

    inst = HoldingTable.HoldingTable(**record)
    print(inst)
    
    count = dbEngine.instance_insert(inst)
    print(count)
    self.assertTrue(True)

  # def test_select_record(self):
  #   results = HoldingTable.holding_insert(99, 1, 'AAPL')
  #   print(results)
  #   self.assertTrue(True)

  def test_scalar(self):
    
    result = dbEngine.select_scalars(select(HoldingTable.HoldingTable.code).where(HoldingTable.HoldingTable.id.in_([1,2,3,4])))
    print(result)
    self.assertTrue(True)

  def test_select_record(self):
    results = dbEngine.select_stmt(select(HoldingTable.HoldingTable).where(HoldingTable.HoldingTable.id.in_([1,2,3,4])))
    # print(results)
    for r in results:
      print(r.id)
      # print(type(r))
      # user_holding = HoldingTable.UserHoldingTable(**r._mapping)
      # print(user_holding)
      # print(r)
      # print(r['id'])
      # print(r.uid)
      # print(r.type)
      # print(r.code)
      # print(r.flag)
      # print(r.created)
      # print(r.updated)
      
    self.assertTrue(True)

  def test_select_holding(self): 
    results = HoldingTable.select_holding(99, type = 1)
    # print(results)
    for r in results:
      print(r.__dict__)
    self.assertTrue(True)

  def test_select_records(self):

    results = HoldingTable.records(99)
    print(results)

    self.assertTrue(True)

  def test_fetch_stock_info(self):
    # Call the fetch_stock_info function
    Info.fetch_stock_info()

    # Verify that data has been inserted into the InfoTable
    results = dbEngine.select_stmt(select(Info.InfoTable).where(Info.InfoTable.type == Info.ITEM_TYPE_STOCK))
    for res in results:
      r = res[0]
      print(r.code, r.name, r.type, r.market)

    # Assert that at least one record exists
    self.assertTrue(len(results) > 0)

  # def test_fetch_table(self):
  #   table = Stock.create_history_table("AAPL", "daily", "qfq")

  #   self.assertTrue(True)

  def test_download_history_data(self):
    # Test data
    code = "000001"  # Example stock code
    start_date = "20230101"
    end_date = "20230131"
    period = "daily"
    adjust = "qfq"

    # Call the download_history_data function
    Stock.download_history_data(code=code, start=start_date, end=end_date, period=period, adjust=adjust)

    code = "000002"
    Stock.download_history_data(code=code, start=start_date, end=end_date, period=period, adjust=adjust)

    # table_name = Data.make_history_data_table_name(Data.TYPE_STOCK, code, period, adjust)
    # print(table_name)
    # table = Data.history_table_map[table_name]
    # results = dbEngine.select_stmt(select(table))
    # for res in results:
    #   r = res[0]
    #   print(r.code, r.name, r.type, r.market)

    # Verify that data has been inserted into the corresponding table
    # table_name = f"stock_{period}_{adjust}_{code}"
    # table = Data.get_history_data_table(2, code, period, adjust)
    # results = dbEngine.select_stmt(select(table))
    # for res in results:
    #   print(res.__dict__)

    # Assert that at least one record exists
    self.assertTrue(True)

  def test_fetch_history_data(self):
    # Test data
    code = "000001"  # Example stock code
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    period = "daily"
    adjust = "qfq"

    # Call the fetch_history_data function
    results = Stock.fetch_history_data(code, start_date, end_date, period, adjust)

    print('================')
    # Print the fetched data
    for record in results:
      print(record.日期, record.开盘)

    # Assert that the results are not empty
    self.assertTrue(len(results) > 0)

  def test_table_export(self):
    model = holding.HoldingTable
    file_name = './app/db/test.json'
    result = dbEngine.export_json(model, file_name)
    print(result)
    self.assertTrue(True)
    
  def test_table_import(self):
    model = holding.HoldingTable
    file_name = './app/db/test.json'
    result = dbEngine.import_json(model, file_name)
    print(result)
    self.assertTrue(True)

  def test_zip(self):
    file_name = './app/db/test.zip'
    files = ['./app/db/funds_operation_table.json', './app/db/funds_table.json']
    with zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED) as zip:
      for file in files:
        zip.write(file)

    self.assertTrue(True)

if __name__ == '__main__':
  unittest.main()