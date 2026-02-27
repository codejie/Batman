"""
KLine (History Data) functionality for EastMoney library.
"""
from typing import List, Dict, Any, Optional
from .core import fetch_and_reassemble
from .urls import BASE_KLINE_URL
from .utils import get_secid

# KLine Period Mapping
# 101: Daily, 102: Weekly, 103: Monthly
PERIOD_MAP = {
    'daily': '101',
    'weekly': '102',
    'monthly': '103'
}

# Adjust Type Mapping
# 0: No adjust, 1: QFQ (Forward), 2: HFQ (Backward)
ADJUST_MAP = {
    'none': '0',
    'qfq': '1',
    'hfq': '2'
}

# KLine Data Fields Mapping (f51-f58 to readable keys)
# Default fields returned by EM KLine API usually are comma-separated strings.
# We need to parse them. EMParser.reassemble handles dict keys, but KLine data 
# is often a list of strings "2023-01-01,10.0,11.0,..." in `klines` field.
# So we need a specialized parser or post-processing.
# For now, let's fetch the raw list and process it.

async def get_kline_data(
    code: str, 
    start_date: str = '19000101', 
    end_date: str = '20991231', 
    period: str = 'daily', 
    adjust: str = 'qfq'
) -> List[Dict[str, Any]]:
    """
    Fetch KLine (historical) data.
    
    :param code: Stock code (e.g. '000001')
    :param start_date: Start date in 'YYYYMMDD' format
    :param end_date: End date in 'YYYYMMDD' format
    :param period: 'daily', 'weekly', 'monthly'
    :param adjust: 'qfq', 'hfq', 'none'
    :return: List of dicts with keys: date, open, close, high, low, volume, turnover, amplitude
    """
    secid = get_secid(code)
    
    # fields1: f1-f6 (metadata, not used much)
    # fields2: f51=Date, f52=Open, f53=Close, f54=High, f55=Low, f56=Vol, f57=Turnover, f58=Amplitude
    fields1 = "f1,f2,f3,f4,f5,f6"
    fields2 = "f51,f52,f53,f54,f55,f56,f57,f58"
    
    params = {
        "secid": secid,
        "klt": PERIOD_MAP.get(period, '101'),
        "fqt": ADJUST_MAP.get(adjust, '1'),
        "beg": start_date,
        "end": end_date,
        "fields1": fields1,
        "fields2": fields2,
        "lmt": "1000000" # limit
    }
    
    # KLine response structure:
    # { "data": { "code": "...", "klines": ["2023-01-01,10.5,10.6,...", ...] } }
    # fetch_and_reassemble isn't directly suitable because "klines" is a list of strings, 
    # not a list of dicts. We need to fetch raw data and parse.
    
    from .client import client
    from .parser import parser
    
    url = BASE_KLINE_URL
    response_data = await client.get(url, params=params)
    
    # Extract 'klines' list
    raw_lines = parser.extract_list(response_data, path="data.klines")
    
    if not raw_lines:
        return []
        
    # Parse lines
    # f51,f52,f53,f54,f55,f56,f57,f58 -> Date, Open, Close, High, Low, Vol, Amt, Amp
    keys = ["date", "open", "close", "high", "low", "volume", "turnover", "amplitude"]
    
    parsed_data = []
    for line in raw_lines:
        parts = line.split(",")
        if len(parts) >= len(keys):
            item = {}
            # Map parts to keys. Note: Types are strings, might want to convert to float/int.
            # For simplicity, keeping as parsed values (usually strings in JSON), 
            # but usually numeric fields should be numbers.
            # Let's do basic conversion.
            item["date"] = parts[0]
            try:
                item["open"] = float(parts[1])
                item["close"] = float(parts[2])
                item["high"] = float(parts[3])
                item["low"] = float(parts[4])
                item["volume"] = float(parts[5])
                item["turnover"] = float(parts[6])
                item["amplitude"] = float(parts[7])
            except (ValueError, IndexError):
                pass # skip or keep partial?
            
            parsed_data.append(item)
            
    return parsed_data
