import logging
from . import mylogger

def logger(module_name: str, loglevel = logging.DEBUG):
    module_logger = mylogger.get_logger(module_name, loglevel = loglevel)
    return module_logger

