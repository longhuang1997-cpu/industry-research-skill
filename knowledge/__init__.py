"""
知识层 - 框架选择器与数据源选择器

根据行业特征自动选择分析框架和数据源
"""

__version__ = "0.1.0-alpha"

# 导出主要类
from .frameworks import FrameworkSelector, CustomFrameworkBuilder
from .data_sources import DataSourceSelector

__all__ = [
    'FrameworkSelector',
    'CustomFrameworkBuilder',
    'DataSourceSelector',
]
