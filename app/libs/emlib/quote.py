"""
Quote functionality for EastMoney library.
"""
from typing import List, Dict, Any
from .core import fetch_and_reassemble
from .urls import BASE_ULIST_URL
from .utils import get_secids

# Field mapping for EastMoney quote API (f-keys to readable names)
# Note: This is a partial mapping based on common usage.
QUOTE_FIELD_MAP = {
    "f12": "code",
    "f14": "name",
    "f2": "close",
    "f3": "change",
    "f4": "change_percent",
    "f5": "volume",
    "f6": "turnover",
    "f15": "high",
    "f16": "low",
    "f17": "open",
    "f18": "prev_close",
    "f19": "total_value", # Total market value
    "f20": "circulating_value", # Circulating market value
    "f21": "float_value" # Check meaning
}

async def get_realtime_quotes(codes: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch real-time quotes for a list of stock codes.
    """
    secids = get_secids(codes)
    
    # Construct params for ulist endpoint
    # fields: Request specific fields. 
    # f12=Code, f14=Name, f2=Close, f3=Change, f4=Change%, f5=Vol, f6=Amt, f15=High, f16=Low, f17=Open, f18=PreClose
    fields = "f12,f14,f2,f3,f4,f5,f6,f15,f16,f17,f18"
    
    params = {
        "secids": secids,
        "fields": fields,
        "invt": "2", # refresh interval hint?
        "fltt": "2", # float precision?
        "fid": "f3", # sort by?
        "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23" # filter string (might need adjustment if strict)
    }
    
    # fetch_and_reassemble expects to find data in "data.diff" usually for ulist, 
    # but let's check response structure. 
    # Usually ulist response: { "data": { "diff": [ ... ] } } or { "data": { "diff": { "0.000001": { ... } } } } depending on version.
    # Actually, ulist with secids often returns a list or dict in diff.
    # Let's assume list in 'data.diff' based on common behavior.
    
    return await fetch_and_reassemble(
        BASE_ULIST_URL, 
        params=params, 
        field_map=QUOTE_FIELD_MAP,
        data_path="data.diff"
    )
