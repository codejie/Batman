"""
Logger
"""
import sys
import logging

stream_handler = logging.StreamHandler(sys.stdout)
# log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(logging.Formatter("[%(asctime)s]%(levelname)s:\t%(message)s"))

logger = logging.getLogger('__name__')
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)