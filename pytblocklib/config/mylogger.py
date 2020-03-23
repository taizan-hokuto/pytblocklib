from logging import NullHandler, getLogger, StreamHandler, FileHandler, Formatter
import logging
from datetime import datetime
from pytblocklib import RELEASE

def get_logger(modname,loglevel=logging.DEBUG):
    logger = getLogger(modname)
    if loglevel == None:
        logger.addHandler(NullHandler())
        return logger
    if RELEASE:
        loglevel = logging.INFO
    logger.setLevel(loglevel)
    #create handler1 for showing info
    handler1 = StreamHandler()
    if RELEASE:
        formatter  = ReleaseFormatter()
    else:
        formatter  = MyFormatter()
    handler1.setFormatter(formatter)

    handler1.setLevel(loglevel) 
    logger.addHandler(handler1)
    #create handler2 for recording log file
    if loglevel <= logging.DEBUG:
        handler2 = FileHandler(filename="log.txt", encoding='utf-8')
        handler2.setLevel(logging.ERROR)
        handler2.setFormatter(MyFormatter())


        logger.addHandler(handler2)
    return logger

class MyFormatter(logging.Formatter):
    def format(self, record):
        timestamp = (
            datetime.fromtimestamp(record.created)).strftime("%m-%d %H:%M:%S")
        module = (record.module).ljust(15)
        funcname = (record.funcName).ljust(18)
        lineno = str(record.lineno).rjust(4)
        message = record.getMessage()
        
        return '{}| {} ( {}:{}) - {}'.format(
            timestamp, module, funcname, lineno, message)

class ReleaseFormatter(logging.Formatter):
    def format(self, record):
        return '{}: {}'.format(record.levelname, record.getMessage())

