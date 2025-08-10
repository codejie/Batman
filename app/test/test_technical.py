import unittest
import pandas as pd
from app.database.data.stock import download_history_data
import app.calc.adx as adx
import app.calc.ma as ma

class TestTechnicalAnalysis(unittest.TestCase):

    def test_ma(self):
        # 1. 获取测试数据
        code = "600057" # "002611"
        start_date = "20240806"
        end_date = "20250806"
        historical_data = download_history_data(code, start_date, end_date)

        result = ma.calc(historical_data)
        # print(result)
        report = ma.report(historical_data, result, idx=None)
        print(report)

        self.assertTrue(True)

    def test_adx(self):
        # 1. 获取测试数据
        code = "600057"
        start_date = "20240806"
        end_date = "20250807"
        data = download_history_data(code, start_date, end_date)
        # print(data)
        options = adx.defaultOptions
        options['period'] = 10
        result = adx.calc(history_data=data, options=options)
        print(result)
        report = adx.report(history_data=data, adx_data=result, options=options)
        print(report)

        # # 2. 打印结果进行验证
        # print(f"\n--- ADX Analysis for {code} ---")
        # print(f"ADX: {result['ADX']}")
        # print(f"+DI: {result['+DI']}")
        # print(f"-DI: {result['-DI']}")
        # print(f"Signal: {result['Signal']}")
        # print("------------------------------------\n")

        # print(len(data))
        # print(len(result))
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()