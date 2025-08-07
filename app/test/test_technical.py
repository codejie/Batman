import unittest
import pandas as pd
from app.calc.ma import get_ma_trend, ma_diff_rank
from app.database.data.stock import download_history_data
import talib
import app.calc.adx as adx

class TestTechnicalAnalysis(unittest.TestCase):

    def test_get_ma_trend(self):
        # 1. 获取测试数据
        # 我们获取一只股票（例如：贵州茅台 600519）过去一年的历史数据
        code = "600519"
        start_date = "2023-08-01"
        end_date = "2024-08-01"
        historical_data = download_history_data(code, start_date, end_date)

        # 确保我们获取到了数据
        self.assertIsNotNone(historical_data, "未能下载历史数据")
        self.assertFalse(historical_data.empty, "下载的历史数据为空")
        
        # 将列名从中文改为英文 '收盘' -> 'close'
        historical_data.rename(columns={'收盘': 'close'}, inplace=True)

        # 2. 定义MA周期
        ma_periods = [20, 60] # 判断20日线和60日线的趋势

        # 3. 调用函数
        trend_result = get_ma_trend(historical_data, ma_periods)

        # 4. 打印结果进行验证
        print(f"\n--- MA Trend Analysis for {code} ---")
        print(f"MA Periods: {ma_periods}")
        print(f"Latest MA Values: {trend_result.get('ma_values')}")
        print(f"Determined Trend: {trend_result.get('trend')}")
        print(f"Analysis: {trend_result.get('analysis')}")
        print("------------------------------------\n")

        # 5. 基本断言
        self.assertIn('ma_values', trend_result)
        self.assertIn('trend', trend_result)
        self.assertIn('analysis', trend_result)
        self.assertTrue(True)

    def test_ma_trend_rank(self):
        # 1. 获取测试数据
        code = "600057" # "002611"
        start_date = "20240806"
        end_date = "20250806"
        historical_data = download_history_data(code, start_date, end_date)

        # 确保我们获取到了数据
        self.assertIsNotNone(historical_data, "未能下载历史数据")
        self.assertFalse(historical_data.empty, "下载的历史数据为空")

        # 将列名从中文改为英文 '收盘' -> 'close'
        historical_data.rename(columns={'收盘': 'close'}, inplace=True)

        # 2. 定义MA周期
        periods = [5, 10, 20, 30, 40, 50, 60]

        # 3. 调用函数
        rank = ma_diff_rank(historical_data['close'], periods)

        # 4. 打印结果进行验证
        print(f"\n--- MA Trend Rank for {code} ---")
        print(f"MA Periods: {periods}")
        print(f"MA Trend Rank: {rank}/{len(periods)}")
        print("------------------------------------\n")

        # 5. 基本断言
        self.assertIsInstance(rank, int)

    def test_ma(self):
        # 1. 获取测试数据
        code = "002728"
        start_date = "20250506"
        end_date = "20250806"
        historical_data = download_history_data(code, start_date, end_date)

        adx = talib.ADX(historical_data['最高'], 
                  historical_data['最低'], 
                  historical_data['收盘'], timeperiod=14)
    
        # print(f"ADX for {code} from {start_date} to {end_date}:")
        # print(adx)

# 计算+DI和-DI
        plus_di = talib.PLUS_DI(historical_data['最高'], historical_data['最低'], historical_data['收盘'], timeperiod=14)
        minus_di = talib.MINUS_DI(historical_data['最高'],  historical_data['最低'],  historical_data['收盘'], timeperiod=14)

        # 将结果添加到DataFrame
        historical_data['ADX'] = adx
        historical_data['+DI'] = plus_di
        historical_data['-DI'] = minus_di

        print(historical_data)

# 判断上升趋势（例如：ADX > 25 且 +DI > -DI）
        historical_data['is_uptrend'] = (historical_data['ADX'] > 25) & (historical_data['+DI'] > historical_data['-DI'])
        print(historical_data[['ADX', '+DI', '-DI', 'is_uptrend']])

        self.assertTrue(True)

    def test_adx(self):
        # 1. 获取测试数据
        code = "600057"
        start_date = "20240806"
        end_date = "20250806"
        data = download_history_data(code, start_date, end_date)

        result = adx.calc(data=data, signal=True)

        # 2. 打印结果进行验证
        print(f"\n--- ADX Analysis for {code} ---")
        print(f"ADX: {result['ADX']}")
        print(f"+DI: {result['+DI']}")
        print(f"-DI: {result['-DI']}")
        print(f"Signal: {result['Signal']}")
        print("------------------------------------\n")

        print(len(data))
        print(len(result))
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()