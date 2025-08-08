import unittest
import pandas as pd
from app.database.data import stock as Stock

# 设置pandas以显示所有列和更宽的列
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

class TestStockDataDownloader(unittest.TestCase):

    def test_download_list(self):
        print("\n--- Testing download_list ---")
        # 该函数没有返回值，但会操作数据库
        Stock.download_list()
        print("download_list executed.")
        self.assertTrue(True)

    def test_download_history_data(self):
        print("\n--- Testing download_history_data ---")
        result = Stock.download_history_data('000001', '2024-01-01', '2024-01-10')
        print(result)
        self.assertTrue(True)

    def test_download_spot_data(self):
        print("\n--- Testing download_spot_data ---")
        result = Stock.download_spot_data(codes=['000001', '600519'])
        print(result)
        self.assertTrue(True)

    def test_download_info(self):
        print("\n--- Testing download_info ---")
        result = Stock.download_info('000001')
        print(result)
        self.assertTrue(True)

    def test_download_financial_abstract_indicator(self):
        print("\n--- Testing download_financial_abstract_indicator ---")
        result = Stock.download_financial_abstract_indicator('000001')
        print(result)
        self.assertTrue(True)

    def test_download_financial_analysis_indicator(self):
        print("\n--- Testing download_financial_analysis_indicator ---")
        result = Stock.download_financial_analysis_indicator('000001')
        print(result)
        self.assertTrue(True)

    def test_download_cash_report_data(self):
        print("\n--- Testing download_cash_report_data ---")
        result = Stock.download_cash_report_data('SH600519')
        print(result)
        self.assertTrue(True)

    def test_download_valuation_indicator(self):
        print("\n--- Testing download_valuation_indicator ---")
        result = Stock.download_valuation_indicator('000001')
        print(result)
        self.assertTrue(True)

    def test_download_performance_report(self):
        print("\n--- Testing download_performance_report ---")
        result = Stock.download_performance_report('000001')
        print(result)
        self.assertTrue(True)

    def test_download_dividend_distribution(self):
        print("\n--- Testing download_dividend_distribution ---")
        result = Stock.download_dividend_distribution('000001')
        print(result)
        self.assertTrue(True)

    def test__download_industry_data(self):
        print("\n--- Testing _download_industry_data ---")
        result = Stock._download_industry_data()
        print(result)
        self.assertTrue(True)

    def test_download_industry_rank(self):
        print("\n--- Testing download_industry_rank ---")
        result = Stock.download_industry_rank()
        print(result)
        self.assertTrue(True)

    def test_download_company_news(self):
        print("\n--- Testing download_company_news ---")
        result = Stock.download_company_news('000001')
        print(result)
        self.assertTrue(True)

    def test_download_company_announcements(self):
        print("\n--- Testing download_company_announcements ---")
        result = Stock.download_company_announcements('000001')
        print(result)
        self.assertTrue(True)

    def test_download_research_report(self):
        print("\n--- Testing download_research_report ---")
        result = Stock.download_research_report('000001')
        print(result)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()