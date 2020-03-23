import configparser
import logging
import os
from . import mylogger

configfile_path = 'config.ini'

def logger(module_name: str, loglevel = logging.DEBUG):
    module_logger = mylogger.get_logger(module_name, loglevel = loglevel)
    return module_logger

