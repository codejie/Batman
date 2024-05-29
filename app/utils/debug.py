"""
系统调试函数
"""
import sys

def __function__() -> str:
    return sys._getframe().f_code.co_name