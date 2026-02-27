"""
Trend (Intraday) functionality for EastMoney library.
"""
from typing import List, Dict, Any, Optional
from .core import fetch_and_reassemble
from .urls import BASE_TREND_URL
from .utils import get_secid

async def get_trend_data(
    code: str, 
    market: int = 1 # 0: SZ, 1: SH. But get_secid handles this based on code usually.
) -> List[Dict[str, Any]]:
    """
    Fetch intraday trend data (minute-by-minute).
    
    :param code: Stock code
    :return: List of dicts with time, price, average, volume, etc.
    """
    secid = get_secid(code)
    
    # fields1: f1-f6
    # fields2: f51=Time, f53=Price, f54=Vol?, f58=AvgPrice?
    # Common fields: f51,f53,f54,f55,f56,f57,f58
    fields1 = "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13"
    fields2 = "f51,f53,f54,f55,f56,f57,f58"
    
    params = {
        "secid": secid,
        "fields1": fields1,
        "fields2": fields2,
        "iscr": "0" # is current?
    }
    
    # Response structure: { "data": { "trends": ["09:30,10.0,10.1,...", ...] } }
    
    from .client import client
    from .parser import parser
    
    url = BASE_TREND_URL
    response_data = await client.get(url, params=params)
    
    raw_lines = parser.extract_list(response_data, path="data.trends")
    
    if not raw_lines:
        return []
        
    # Parse lines
    # f51,f53,f54,f55,f56,f57,f58 -> Time, Price, Vol?, ?, AvgPrice?
    # Based on observation:
    # 0: Time (09:30)
    # 1: Price
    # 2: Volume?
    # 3: ?
    # 4: Avg Price
    
    # Let's map to generic keys for now
    keys = ["time", "price", "volume", "item3", "avg_price", "item5", "item6"]
    
    parsed_data = []
    for line in raw_lines:
        parts = line.split(",")
        if len(parts) >= 2: # At least time and price
            item = {}
            item["time"] = parts[0]
            try:
                item["price"] = float(parts[1])
                if len(parts) > 2: item["volume"] = float(parts[2])
                if len(parts) > 4: item["avg_price"] = float(parts[4])
            except (ValueError, IndexError):
                pass
            parsed_data.append(item)
            
    return parsed_data
