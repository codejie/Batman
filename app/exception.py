"""
Exception
"""
class AppException(Exception):
    def __init__(self, code: int = -1, message: str | None = None) -> None:
        self.code = code
        self.message = message

    def __init__(self, e: Exception) -> None:
        self.code = -1
        self.message = str(e)

# class AppRouterException(AppException):
#     def __init__(self, code: int = -1, message: str | None = None) -> None:
#         super.__init__(message)
#         self.code = code

#     def __init__(self, e: Exception):
#         super.__init__(e)
#         self.code = -1

# class AppException(AppException):
#     pass
