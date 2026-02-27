"""
Core functionality for EastMoney library.
"""
from typing import Any, Dict, List, Optional
from .client import client as em_client
from .parser import parser as em_parser
from app.exception import AppException
from app.logger import logger

async def fetch_and_reassemble(
    url: str, 
    params: Optional[Dict[str, Any]] = None, 
    field_map: Optional[Dict[str, str]] = None,
    data_path: str = "data"
) -> List[Dict[str, Any]]:
    """
    Combined operation for fetching and reassembling data from EastMoney API.
    
    1. Assemble URL (handled by client.get)
    2. Make HTTP GET request
    3. Analyze/extract the target list from the response
    4. Reassemble each item based on the field_map
    """
    try:
        # Step 1 & 2: Assemble URL and fetch data
        response_data = await em_client.get(url, params=params)
        
        # Step 3: Analyze and extract data list
        raw_list = em_parser.extract_list(response_data, path=data_path)
        
        if not raw_list:
            logger.warning(f"EMLib: No data found at path '{data_path}' for URL {url}")
            return []
            
        # Step 4: Reassemble if field_map is provided
        if field_map:
            return em_parser.reassemble(raw_list, field_map)
        
        return raw_list
        
    except Exception as e:
        logger.error(f"EMLib Error: {repr(e)}")
        raise AppException(-1, f"EMLib operation failed: {repr(e)}")
