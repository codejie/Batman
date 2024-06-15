"""
Exception
"""
class AppException(Exception):
    message: str = None

    def __init__(self, message: str | None = None) -> None:
        self.message = message

    def __init__(self, e: Exception) -> None:
        self.message(str(e))

class AppRouterException(AppException):
    code: int = 0
    
    def __init__(self, code: int = -1, message: str | None = None) -> None:
        super(message)
        self.code = code

    def __init__(self, e: Exception):
        super(e)
        self.code = -1

class AppDataException(AppException):
    pass
