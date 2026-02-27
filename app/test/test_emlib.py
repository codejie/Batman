"""
Tests for app.libs.emlib
"""
import unittest
import asyncio
from unittest.mock import patch, MagicMock
from app.libs.emlib import get_realtime_quotes, EMClient, EMParser, fetch_and_reassemble

class TestEMLib(unittest.TestCase):
    
    def test_utils(self):
        from app.libs.emlib.utils import get_secid, get_secids
        self.assertEqual(get_secid("000001"), "0.000001")
        self.assertEqual(get_secid("600000"), "1.600000")
        self.assertEqual(get_secid("300059"), "0.300059")
        self.assertEqual(get_secids(["000001", "600000"]), "0.000001,1.600000")

    @patch("app.libs.emlib.client.EMClient.get", new_callable=MagicMock)
    def test_get_realtime_quotes(self, mock_get):
        # Mock response data for get_realtime_quotes
        mock_response = {
            "data": {
                "diff": [
                    {"f12": "000001", "f14": "Ping An Bank", "f2": 10.5, "f3": 0.1, "f4": 0.96},
                    {"f12": "600000", "f14": "SPD Bank", "f2": 7.2, "f3": -0.05, "f4": -0.69}
                ]
            }
        }
        
        # Setup mock to behave like an async function
        f = asyncio.Future()
        f.set_result(mock_response)
        mock_get.return_value = f

        # Run async function in sync test
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            from app.libs.emlib import get_realtime_quotes
            result = loop.run_until_complete(get_realtime_quotes(["000001", "600000"]))
        finally:
            loop.close()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['code'], "000001")
        self.assertEqual(result[0]['name'], "Ping An Bank")
        self.assertEqual(result[0]['close'], 10.5)
        self.assertEqual(result[1]['code'], "600000")

    @patch("app.libs.emlib.client.EMClient.get", new_callable=MagicMock)
    def test_get_kline_data(self, mock_get):
        # Mock response for get_kline_data
        mock_response = {
            "data": {
                "klines": [
                    "2023-01-01,10.0,11.0,12.0,9.0,1000,10000,5.0",
                    "2023-01-02,11.0,12.0,13.0,10.0,2000,20000,6.0"
                ]
            }
        }
        
        f = asyncio.Future()
        f.set_result(mock_response)
        mock_get.return_value = f

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            from app.libs.emlib import get_kline_data
            result = loop.run_until_complete(get_kline_data("000001"))
        finally:
            loop.close()
            
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['date'], "2023-01-01")
        self.assertEqual(result[0]['open'], 10.0)
        self.assertEqual(result[0]['close'], 11.0)
        
    @patch("app.libs.emlib.client.EMClient.get", new_callable=MagicMock)
    def test_get_stock_list(self, mock_get):
        # Mock response for get_stock_list
        mock_response = {
            "data": {
                "diff": [
                    {"f12": "000001", "f14": "Stock A", "f2": 10.0},
                    {"f12": "000002", "f14": "Stock B", "f2": 20.0}
                ]
            }
        }
        
        f = asyncio.Future()
        f.set_result(mock_response)
        mock_get.return_value = f

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            from app.libs.emlib import get_stock_list
            result = loop.run_until_complete(get_stock_list(page_index=1, page_size=20))
        finally:
            loop.close()
            
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['code'], "000001")
        self.assertEqual(result[0]['name'], "Stock A")

    @patch("app.libs.emlib.client.EMClient.get", new_callable=MagicMock)
    def test_get_trend_data(self, mock_get):
        # Mock response for get_trend_data
        mock_response = {
            "data": {
                "trends": [
                    "09:30,10.0,1000,0,10.05",
                    "09:31,10.1,2000,0,10.08"
                ]
            }
        }
        
        f = asyncio.Future()
        f.set_result(mock_response)
        mock_get.return_value = f

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            from app.libs.emlib import get_trend_data
            result = loop.run_until_complete(get_trend_data("000001"))
        finally:
            loop.close()
            
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['time'], "09:30")
        self.assertEqual(result[0]['price'], 10.0)
        self.assertEqual(result[0]['volume'], 1000.0)
        self.assertEqual(result[0]['avg_price'], 10.05)
        
    def test_parser_extract(self):
        data = {"a": {"b": [1, 2, 3]}}
        extracted = EMParser.extract_list(data, "a.b")
        self.assertEqual(extracted, [1, 2, 3])
        
        extracted_empty = EMParser.extract_list(data, "a.c")
        self.assertEqual(extracted_empty, [])

    def test_parser_reassemble(self):
        data = [{"id": 1, "val": 10}, {"id": 2, "val": 20}]
        field_map = {"id": "code", "val": "price"}
        reassembled = EMParser.reassemble(data, field_map)
        
        self.assertEqual(reassembled[0]['code'], 1)
        self.assertEqual(reassembled[0]['price'], 10)
        self.assertEqual(reassembled[1]['code'], 2)

if __name__ == '__main__':
    unittest.main()
