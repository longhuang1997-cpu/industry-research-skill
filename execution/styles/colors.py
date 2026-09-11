"""
配色方案管理器

功能:
1. 根据行业自动选择配色方案
2. 提供统一的颜色获取接口
3. 支持配色方案扩展
"""

from typing import Dict, List, Optional
from abc import ABC, abstractmethod


class ColorScheme(ABC):
    """
    配色方案基类

    所有行业配色方案必须继承此类
    """

    @abstractmethod
    def get_primary(self) -> str:
        """获取主色"""
        pass

    @abstractmethod
    def get_secondary(self) -> str:
        """获取辅助色"""
        pass

    @abstractmethod
    def get_background(self) -> str:
        """获取背景色"""
        pass

    @abstractmethod
    def get_gradient(self, steps: int = 5) -> List[str]:
        """
        获取渐变色序列

        Args:
            steps: 渐变步数

        Returns:
            colors: 颜色列表（HEX格式）
        """
        pass

    @abstractmethod
    def get_categorical(self, n: int = 5) -> List[str]:
        """
        获取分类配色

        Args:
            n: 需要的颜色数量

        Returns:
            colors: 颜色列表（HEX格式）
        """
        pass


class DefaultColorScheme(ColorScheme):
    """
    默认配色方案（通用）

    适用于未指定行业的场景
    """

    def get_primary(self) -> str:
        return '#3b82f6'  # 蓝色

    def get_secondary(self) -> str:
        return '#60a5fa'  # 浅蓝色

    def get_background(self) -> str:
        return '#f8fafc'  # 浅灰色背景

    def get_gradient(self, steps: int = 5) -> List[str]:
        """蓝色渐变"""
        return [
            '#1e3a8a',  # 深蓝
            '#2563eb',
            '#3b82f6',
            '#60a5fa',
            '#93c5fd'   # 浅蓝
        ][:steps]

    def get_categorical(self, n: int = 5) -> List[str]:
        """分类配色"""
        colors = [
            '#3b82f6',  # 蓝色
            '#10b981',  # 绿色
            '#f59e0b',  # 橙色
            '#ef4444',  # 红色
            '#8b5cf6',  # 紫色
            '#ec4899',  # 粉色
            '#06b6d4',  # 青色
            '#84cc16'   # 黄绿色
        ]
        return colors[:n]

    def get_positive_color(self) -> str:
        """正向指标颜色"""
        return '#10b981'  # 绿色

    def get_negative_color(self) -> str:
        """负向指标颜色"""
        return '#ef4444'  # 红色

    def get_neutral_color(self) -> str:
        """中性指标颜色"""
        return '#6b7280'  # 灰色


class ColorSchemeManager:
    """
    配色方案管理器

    根据行业类型自动选择合适的配色方案
    """

    def __init__(self):
        """初始化管理器"""
        self._schemes: Dict[str, ColorScheme] = {}
        self._register_default_schemes()

    def _register_default_schemes(self):
        """注册默认配色方案"""
        from .medical import MedicalColorScheme
        from .finance import FinanceColorScheme
        from .tech import TechColorScheme

        self.register('default', DefaultColorScheme())
        self.register('medical', MedicalColorScheme())
        self.register('healthcare', MedicalColorScheme())  # 别名
        self.register('finance', FinanceColorScheme())
        self.register('tech', TechColorScheme())
        self.register('technology', TechColorScheme())  # 别名

    def register(self, industry: str, scheme: ColorScheme):
        """
        注册配色方案

        Args:
            industry: 行业名称（小写）
            scheme: 配色方案实例
        """
        self._schemes[industry.lower()] = scheme

    def get_scheme(self, industry: str) -> ColorScheme:
        """
        获取配色方案

        Args:
            industry: 行业名称

        Returns:
            scheme: 配色方案实例
        """
        industry_key = industry.lower()

        # 精确匹配
        if industry_key in self._schemes:
            return self._schemes[industry_key]

        # 模糊匹配
        for key, scheme in self._schemes.items():
            if key in industry_key or industry_key in key:
                return scheme

        # 默认配色
        return self._schemes['default']


def main():
    """测试配色方案管理器"""
    print("="*60)
    print("测试: 配色方案管理器")
    print("="*60)

    manager = ColorSchemeManager()

    # 测试不同行业
    industries = ['医疗陪护', 'finance', 'tech', '未知行业']

    for industry in industries:
        print(f"\n行业: {industry}")
        scheme = manager.get_scheme(industry)
        print(f"  主色: {scheme.get_primary()}")
        print(f"  辅助色: {scheme.get_secondary()}")
        print(f"  背景色: {scheme.get_background()}")
        print(f"  渐变色: {scheme.get_gradient(3)}")
        print(f"  分类色: {scheme.get_categorical(3)}")


if __name__ == '__main__':
    main()
