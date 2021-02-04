from ctypes import ArgumentError
import enum

import re
from re import RegexFlag
import datetime
import os
import threading
import sys

if sys.platform == "win32":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

FILE = open('LogPython_info.log', 'a')
pid = str(os.getpid()).ljust(5)

RESET_COLOR = '\033[0m' 

DEBUG_COLOR = '\033[36m'
INFO_COLOR = '\033[32m'
WARNING_COLOR = '\033[33m'
ERROR_COLOR = '\033[31m'

LOCK = threading.Lock()

class LEVEL(enum.IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

__console_level__ = LEVEL.INFO
__file_level__ = LEVEL.DEBUG

class LogManager:
    @staticmethod
    def prefix(level: str) -> str:
        level = level.ljust(7)
        return f"[{datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}] [{__name__} {pid}] [{level}]"

    @staticmethod
    def set_console_level(level: LEVEL):
        if type(level) is LEVEL:
            global __console_level__
            __console_level__ = level
        else:
            raise ArgumentError()

    @staticmethod
    def set_file_level(level: LEVEL):
        if type(level) is LEVEL:
            global __file_level__
            __file_level__ = level
        else:
            raise ArgumentError()

    @staticmethod
    def log(color: str, level: LEVEL, level_str: str, *args, **kwargs):

        if level.value >= __console_level__:
            LOCK.acquire()

            try:
                print(' ' + color + LogManager.prefix(level_str) + ' ', end='')
                print(*args, **kwargs)
                print(RESET_COLOR, end='')
            except:
                pass

            LOCK.release()

        if level.value >= __file_level__:
            try:
                print(LogManager.prefix(level_str) + ' ', end='', file=FILE)
                print(*args, **kwargs, file=FILE)
            except:
                print('!!! FAILED TO LOG DATA !!!', file=FILE)
                
            FILE.flush()

    @staticmethod
    def debug(*args, **kwargs):

        LogManager.log(DEBUG_COLOR, LEVEL.DEBUG, 'DEBUG', *args, **kwargs)

    @staticmethod
    def info(*args, **kwargs):

        LogManager.log(INFO_COLOR, LEVEL.INFO, 'INFO', *args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs):

        LogManager.log(WARNING_COLOR, LEVEL.WARNING,
                       'WARNING', *args, **kwargs)

    @staticmethod
    def error(*args, **kwargs):

        LogManager.log(ERROR_COLOR, LEVEL.ERROR, 'ERROR', *args, **kwargs)
        
    @staticmethod
    def _input(*args, **kwargs):
        
        return ' ' + input(LogManager.prefix('INPUT') + ' [you]') + ' \n'
    
    @staticmethod
    def _output(*args, **kwargs):
        
        return ' ' + input(LogManager.prefix('OUTPUT')) + ' '

    @staticmethod
    def get_logs(qantiny:int, *args) -> list:
        
        _ = open("LogPython_info.log", "r").readlines()
        
        res = list()
        
        res.append(_[len(_) - qantiny:])
        
        return res

    class get_errors:

        def __init__(self):

            reg = r"\{ERROR\} \: ([^+]+?)\{ShGLogger v 1\.0\}"

            file = open('LogPython_info.log', 'r')
            text = file.read()

            matches = re.findall(reg, text, RegexFlag.MULTILINE)

            completed = []

            for item in matches:
                completed.append(item.replace('{ShGLogger v 1.0}', ''))

            self.completed = completed

        def __str__(self) -> str:
            return str(self.completed[len(self.completed) - 1])