"""
Stock List functionality for EastMoney library.
"""
from typing import List, Dict, Any, Optional
from .core import fetch_and_reassemble
from .urls import BASE_LIST_URL

# Field mapping for Stock List (similar to Quote but for list)
LIST_FIELD_MAP = {
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
    "f20": "total_value", # Total market value
    "f21": "circulating_value", # Circulating market value
    "f23": "pb", # Price-to-Book
    "f24": "roe", # Return on Equity
    "f25": "pe_ttm" # PE (TTM)
}

async def get_stock_list(
    page_index: int = 1,
    page_size: int = 20,
    sort_by: str = "f3", # Default sort by change percent
    sort_asc: bool = False,
    node: str = "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23" # Default A-share stocks
) -> List[Dict[str, Any]]:
    """
    Fetch a list of stocks with pagination and sorting.
    
    :param page_index: Page number (1-based)
    :param page_size: Number of items per page
    :param sort_by: Field to sort by (e.g. 'f3' for change percent)
    :param sort_asc: True for ascending, False for descending
    :param node: Filter string for market/type
    :return: List of stock data dicts
    """
    
    # fields: Request specific fields.
    fields = "f12,f14,f2,f3,f4,f5,f6,f15,f16,f17,f18,f20,f21,f23,f24,f25"
    
    params = {
        "pn": page_index,
        "pz": page_size,
        "po": "1" if sort_asc else "0",
        "np": "1",
        "fltt": "2",
        "invt": "2",
        "fid": sort_by,
        "fs": node,
        "fields": fields
    }
    
    return await fetch_and_reassemble(
        BASE_LIST_URL, 
        params=params, 
        field_map=LIST_FIELD_MAP,
        data_path="data.diff"
    )
