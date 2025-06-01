"""
Exception
"""
from typing import Optional

class AppException(Exception):
    def __init__(self, e: Optional[Exception] = None, code: int = -1, message: Optional[str] = None) -> None:
        self.code = -1
        self.message = str(e)