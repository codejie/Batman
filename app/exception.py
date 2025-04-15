"""
Exception
"""
class AppException(Exception):
    def __init__(self, code: int = -1, message: str = None) -> None:
        self.code = code
        self.message = message

    def __init__(self, e: Exception) -> None:
        self.code = -1
        self.message = str(e)