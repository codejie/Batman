import httpx
import json
from typing import Any, Dict, Optional, Union
from app.exception import AppException
from app.logger import logger

class EMClient:
    """
    HTTP Client for fetching data with URL assembly and base response handling.
    """
    DEFAULT_TIMEOUT = 10.0
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Referer": "https://quote.eastmoney.com/",
    }

    @staticmethod
    def assemble_url(base_url: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Assemble the final URL with query parameters.
        """
        if not params:
            return base_url
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        separator = "&" if "?" in base_url else "?"
        return f"{base_url}{separator}{query_string}"

    async def get(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None, 
        headers: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None
    ) -> Any:
        """
        Make an asynchronous HTTP GET request.
        """
        final_headers = self.DEFAULT_HEADERS.copy()
        if headers:
            final_headers.update(headers)

        try:
            async with httpx.AsyncClient(headers=final_headers, verify=False) as client:
                response = await client.get(
                    url, 
                    params=params, 
                    timeout=timeout or self.DEFAULT_TIMEOUT
                )
                response.raise_for_status()
                
                # Check for JSONP responses (common in EastMoney APIs)
                content = response.text
                if content.startswith("jQuery") or "(" in content and content.endswith(");"):
                    # Basic JSONP extraction
                    start = content.find("(") + 1
                    end = content.rfind(")")
                    if start > 0 and end > start:
                        return json.loads(content[start:end])
                
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"EMClient: HTTP status error: {e.response.status_code} for URL {url}")
            raise AppException(-1, f"HTTP status error: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"EMClient: Request error: {repr(e)} for URL {url}")
            raise AppException(-1, f"HTTP request failed: {repr(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"EMClient: JSON decode error: {repr(e)} for URL {url}")
            raise AppException(-1, f"Failed to parse response as JSON: {repr(e)}")
        except Exception as e:
            logger.error(f"EMClient: Unexpected error: {repr(e)} for URL {url}")
            raise AppException(-1, f"Unexpected error during fetch: {repr(e)}")

client = EMClient()
