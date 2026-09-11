"""
配色方案模块

提供行业专用配色方案，确保图表视觉统一性
"""

from .colors import ColorSchemeManager
from .medical import MedicalColorScheme
from .finance import FinanceColorScheme
from .tech import TechColorScheme

__all__ = [
    'ColorSchemeManager',
    'MedicalColorScheme',
    'FinanceColorScheme',
    'TechColorScheme'
]
