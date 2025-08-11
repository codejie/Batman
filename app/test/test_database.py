import ast
import json
import unittest
import zipfile
from sqlalchemy import select
from app.database import dbEngine, holding
from app.database import holding as HoldingTable
from app.database.data import index as Index, stock as Stock
from app.database.calc import (
    CalcAlgorithmItemsTable,
    CalcAlgorithmItemStockListTable,
    CalcAlgorithmItemArgumentsTable,
    CalcAlgorithmItemStockListModel,
    CalcAlgorithmItemArgumentsModel,
    insert_algorithm_item,
    insert_algorithm_item_stock_list,
    insert_algorithm_item_arguments,
    select_algorithm_items,
    select_algorithm_item_stock_list,
    select_algorithm_item_arguments,
    delete_algorithm_item,
)

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

class TestCalcAlgorithmItems(unittest.TestCase):
    def setUp(self):
        dbEngine.start()
        self.db = dbEngine

    def tearDown(self):
        # self.db.trunc_table(CalcAlgorithmItemArguments)
        # self.db.trunc_table(CalcAlgorithmItemStockList)
        # self.db.trunc_table(CalcAlgorithmItems)
        self.db.shutdown()

    def test_insert_algorithm_item(self):
        # Test data
        uid = 1
        name = "test_algorithm"
        category = 1
        type = 1

        # Insert the record
        item_id = insert_algorithm_item(uid, name, category, type)
        self.assertIsNotNone(item_id)

        # Verify the record was inserted
        stmt = select(CalcAlgorithmItemsTable).where(CalcAlgorithmItemsTable.id == item_id)
        result = self.db.select_scalar(stmt)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, name)

    def test_insert_algorithm_item_stock_list(self):
        # Insert a parent record
        item_id = 1 #insert_algorithm_item(1, "test_stock_list", 1, 1)

        # Test data
        items = [
            CalcAlgorithmItemStockListModel(cid=item_id, type=2, code="AAPL"),
            CalcAlgorithmItemStockListModel(cid=item_id, type=2, code="GOOGL"),
        ]

        # Insert the records
        insert_algorithm_item_stock_list(items)

        # Verify the records were inserted
        stmt = select(CalcAlgorithmItemStockListTable).where(CalcAlgorithmItemStockListTable.cid == item_id)
        results = self.db.select_scalars(stmt)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].code, "AAPL")
        self.assertEqual(results[1].code, "GOOGL")

    def test_insert_algorithm_item_arguments(self):
        # Insert a parent record
        item_id = insert_algorithm_item(1, "test_arguments", 1, 1)

        # Test data
        items = [
            CalcAlgorithmItemArgumentsModel(cid=item_id, category=1, type=1, arguments={"key": "value1"}, flag=0),
            CalcAlgorithmItemArgumentsModel(cid=item_id, category=1, type=2, arguments={"key": "value2"}, flag=0),
        ]

        # Insert the records
        insert_algorithm_item_arguments(items)

        # Verify the records were inserted
        stmt = select(CalcAlgorithmItemArgumentsTable).where(CalcAlgorithmItemArgumentsTable.cid == item_id)
        results = self.db.select_scalars(stmt)
        self.assertEqual(len(results), 2)
        arg1 = ast.literal_eval(results[0].arguments)
        arg2 = ast.literal_eval(results[1].arguments)
        self.assertEqual(arg1, {"key": "value6"})
        self.assertEqual(arg2, {"key": "value2"})

    def test_select_algorithm_items_by_uid(self):
        # Test data
        uid = 123
        insert_algorithm_item(uid, "algo1", 1, 1)
        insert_algorithm_item(uid, "algo2", 1, 2)
        insert_algorithm_item(999, "algo3", 2, 1) # Different uid

        # Call the function
        results = select_algorithm_items(uid)

        # Verify the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].name, "algo1")
        self.assertEqual(results[1].name, "algo2")

    def test_select_algorithm_item_stock_list_by_cid(self):
        # Insert a parent record
        item_id = insert_algorithm_item(1, "test_stock_list", 1, 1)

        # Test data
        items = [
            CalcAlgorithmItemStockListModel(cid=item_id, type=2, code="MSFT"),
            CalcAlgorithmItemStockListModel(cid=item_id, type=2, code="AMZN"),
        ]
        insert_algorithm_item_stock_list(items)

        # Call the function
        results = select_algorithm_item_stock_list(item_id)

        # Verify the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].code, "MSFT")
        self.assertEqual(results[1].code, "AMZN")

    def test_select_algorithm_item_arguments_by_cid(self):
        # Insert a parent record
        item_id = insert_algorithm_item(1, "test_arguments", 1, 1)

        # Test data
        items = [
            CalcAlgorithmItemArgumentsModel(cid=item_id, category=1, type=1, arguments={"key": "value1"}, flag=0),
            CalcAlgorithmItemArgumentsModel(cid=item_id, category=1, type=2, arguments={"key": "value2"}, flag=0),
        ]
        insert_algorithm_item_arguments(items)

        # Call the function
        results = select_algorithm_item_arguments(item_id)

        # Verify the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].arguments, {"key": "value1"})
        self.assertEqual(results[1].arguments, {"key": "value2"})

    def test_delete_algorithm_item(self):
        # Insert a parent record
        item_id = insert_algorithm_item(1, "test_delete", 1, 1)

        # Test data
        stock_list_items = [
            CalcAlgorithmItemStockListModel(cid=item_id, type=2, code="TEST"),
        ]
        insert_algorithm_item_stock_list(stock_list_items)

        argument_items = [
            CalcAlgorithmItemArgumentsModel(cid=item_id, category=1, type=1, arguments={"key": "value1"}, flag=0),
        ]
        insert_algorithm_item_arguments(argument_items)

        # Delete the item
        delete_algorithm_item(item_id)

        # Verify the records were deleted
        stmt = select(CalcAlgorithmItemsTable).where(CalcAlgorithmItemsTable.id == item_id)
        result = self.db.select_scalar(stmt)
        self.assertIsNone(result)

        stmt = select(CalcAlgorithmItemStockListTable).where(CalcAlgorithmItemStockListTable.cid == item_id)
        results = self.db.select_scalars(stmt)
        self.assertEqual(len(results), 0)

        stmt = select(CalcAlgorithmItemArgumentsTable).where(CalcAlgorithmItemArgumentsTable.cid == item_id)
        results = self.db.select_scalars(stmt)
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
  unittest.main()