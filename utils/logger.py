"""
日志工具模块

提供统一的日志输出接口
"""

import sys
from datetime import datetime
from enum import Enum
from typing import Optional


class LogLevel(Enum):
    """日志级别"""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class Logger:
    """
    日志工具类
    """

    def __init__(self, name: str = 'industry-research', level: LogLevel = LogLevel.INFO):
        """
        初始化日志器

        Args:
            name: 日志器名称
            level: 日志级别
        """
        self.name = name
        self.level = level

    def _log(self, level: LogLevel, message: str, prefix: str = ''):
        """
        内部日志方法

        Args:
            level: 日志级别
            message: 日志消息
            prefix: 前缀符号
        """
        if level.value >= self.level.value:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] [{self.name}] {prefix}{message}", file=sys.stderr)

    def debug(self, message: str):
        """调试日志"""
        self._log(LogLevel.DEBUG, message, '[DEBUG] ')

    def info(self, message: str):
        """信息日志"""
        self._log(LogLevel.INFO, message, '[INFO] ')

    def warning(self, message: str):
        """警告日志"""
        self._log(LogLevel.WARNING, message, '[WARNING] ')

    def error(self, message: str):
        """错误日志"""
        self._log(LogLevel.ERROR, message, '[ERROR] ')
