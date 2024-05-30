"""
系统调试函数
Note: only in DEBUG mode
"""
import inspect

__DEBUG__ = True

def __function__() -> str:
    if not __DEBUG__:
        return ''
    (
        filename,
        line_number,
        function_name,
        lines,
        index,
    ) = inspect.getframeinfo(inspect.currentframe().f_back)

    return function_name
    # return sys._getframe().f_code.co_name