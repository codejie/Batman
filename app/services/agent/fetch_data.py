"""HTTP fetch utility module for making API requests."""

import requests
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel
from requests.exceptions import RequestException

# Base URL for HTTP requests
base_url: str = "http://localhost:8000"

# Token for authentication (constant value)
token: str = "token-1"


class LoginResult(BaseModel):
    """Model for login result."""
    accessToken: str
    refreshToken: Optional[str] = None
    expired: Optional[datetime] = None
    avatar: Optional[str] = None


class LoginResponse(BaseModel):
    """Response model for login endpoint."""
    result: LoginResult


class UserHoldingRecord(BaseModel):
    """Model for a user holding record."""
    id: int
    type: int  # 1: 指数, 2: 股票
    code: str  # Stock code
    name: str  # Stock name
    flag: int
    created: datetime
    updated: datetime
    quantity: int
    expense: float


class ListHoldingResponse(BaseModel):
    """Response model for list holding endpoint."""
    result: List[UserHoldingRecord]


class RecordRequest(BaseModel):
    """Request model for record endpoint."""
    id: Optional[int] = None
    type: Optional[int] = None
    code: Optional[str] = None
    flag: Optional[int] = None


class RecordResponse(BaseModel):
    """Response model for record endpoint."""
    result: List[UserHoldingRecord] = []


class HistoryData(BaseModel):
    """Model for K-line/history data."""
    日期: str
    开盘: float
    收盘: float
    最高: float
    最低: float
    成交量: float
    成交额: float
    振幅: float
    涨跌幅: float
    涨跌额: float
    换手率: float

    class Config:
        """Pydantic config to allow Chinese field names."""
        populate_by_name = True


class GetHistoryDataRequest(BaseModel):
    """Request model for get history data endpoint."""
    type: int
    code: str
    start: Optional[str] = None
    end: Optional[str] = None
    period: Optional[str] = "daily"
    adjust: Optional[str] = None
    limit: Optional[int] = None
    record_flag: Optional[int] = 0  # 0: normal check & update; 1: disabled, no check and update


class GetHistoryDataResponse(BaseModel):
    """Response model for get history data endpoint."""
    result: List[HistoryData] = []


def _ensure_token() -> bool:
    """
    Check if token is available.
    
    Returns:
        True if token is available, False otherwise
    """
    return bool(token)


def _get_headers() -> Dict[str, str]:
    """
    Get headers with token.
    
    Returns:
        Dictionary with authorization headers
    """
    return {"X-Token": token}


def post(endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
    """
    Make a POST request to the specified endpoint.
    
    Args:
        endpoint: The API endpoint path
        data: Form data
        json: JSON body data
        **kwargs: Additional arguments to pass to requests.post()
    
    Returns:
        Response JSON as dictionary
    """
    try:
        url = f"{base_url}/{endpoint.lstrip('/')}"
        headers = kwargs.pop("headers", {})
        headers.update(_get_headers())
        response = requests.post(url, data=data, json=json, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        return {"error": str(e), "status": "failed"}


def set_base_url(url: str) -> None:
    """
    Set the base URL for HTTP requests.
    
    Args:
        url: The new base URL
    """
    global base_url
    base_url = url


def set_token(new_token: str) -> None:
    """
    Set the authentication token.
    
    Args:
        new_token: The authentication token
    """
    global token
    token = new_token


def get_type(category: str) -> int:
    """
    Get the type value for a given category.
    
    Args:
        category: Category string - '指数'/'index' for index, '股票'/'stock' for stock
    
    Returns:
        1 for index (指数/index), 2 for stock (股票/stock)
    """
    category_lower = category.lower().strip()
    
    if category_lower in ["指数", "index"]:
        return 1
    elif category_lower in ["股票", "stock"]:
        return 2
    else:
        raise ValueError(f"Invalid category: {category}. Use '指数'/'index' or '股票'/'stock'")
def login() -> Dict[str, Any]:
    """
    Login to the service and retrieve authentication token.
    
    Returns:
        Response containing token in result.accessToken
    """
    global token
    
    try:
        url = f"{base_url}/account/login"
        response = requests.post(url)
        response.raise_for_status()
        response_data = response.json()
        
        # Validate response structure
        validated = LoginResponse(**response_data)
        token = validated.result.accessToken
        
        return {
            "status": "success",
            "result": validated.result.dict()
        }
    except RequestException as e:
        return {"error": str(e), "status": "failed"}
    except Exception as e:
        return {"error": f"Login failed: {str(e)}", "status": "failed"}


def list_holding() -> Dict[str, Any]:
    """
    Get the list of holding stocks.
    
    Returns:
        Response containing holding stock list with validated UserHoldingRecord objects
    """
    response = post("/holding/list", {})
    if "error" in response:
        return response
    
    try:
        validated = ListHoldingResponse(**response)
        return {
            "result": [record.dict() for record in validated.result],
            "status": "success"
        }
    except Exception as e:
        return {"error": f"Data validation failed: {str(e)}", "status": "failed"}


def record(id: Optional[int] = None, type: Optional[int] = None, code: Optional[str] = None) -> Dict[str, Any]:
    """
    Get detailed holding stock records with flag set to 1.
    
    Args:
        id: Optional record id
        type: Optional stock type
        code: Optional stock code
    
    Returns:
        Response containing detailed holding stock records
    """
    request_data = {
        "flag": 1
    }
    
    if id is not None:
        request_data["id"] = id
    if type is not None:
        request_data["type"] = type
    if code is not None:
        request_data["code"] = code
    
    response = post("/holding/record", json=request_data)
    if "error" in response:
        return response
    
    try:
        validated = RecordResponse(**response)
        return {
            "result": [record.dict() for record in validated.result],
            "status": "success"
        }
    except Exception as e:
        return {"error": f"Data validation failed: {str(e)}", "status": "failed"}


def get_history_data(type: int, code: str, start: Optional[str] = None, end: Optional[str] = None, 
                     period: Optional[str] = "daily", adjust: Optional[str] = None, 
                     limit: Optional[int] = None, record_flag: Optional[int] = 0) -> Dict[str, Any]:
    """
    Get K-line/history data for a specified stock.
    
    Args:
        type: Stock type (required)
        code: Stock code (required)
        start: Start date (optional)
        end: End date (optional)
        period: Data period, default "daily" (optional)
        adjust: Adjust type (optional)
        limit: Data limit (optional)
        record_flag: 0 for normal check & update, 1 for disabled (optional, default 0)
    
    Returns:
        Response containing K-line/history data records
    """
    request_data = {
        "type": type,
        "code": code,
        "period": period,
        "record_flag": record_flag
    }
    
    if start is not None:
        request_data["start"] = start
    if end is not None:
        request_data["end"] = end
    if adjust is not None:
        request_data["adjust"] = adjust
    if limit is not None:
        request_data["limit"] = limit
    
    response = post("/data/get_history_data", json=request_data)
    if "error" in response:
        return response
    
    try:
        validated = GetHistoryDataResponse(**response)
        return {
            "result": [data.dict() for data in validated.result],
            "status": "success"
        }
    except Exception as e:
        return {"error": f"Data validation failed: {str(e)}", "status": "failed"}
