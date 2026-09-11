"""
金融行业配色方案

配色理念:
- 主色：金融蓝（#1e40af）- 专业、稳重、信任
- 辅助色：科技蓝（#3b82f6）- 创新、科技
- 深色背景：#0f172a - 高端、神秘
- 适用场景：银行、保险、证券、金融科技
"""

from typing import List
from .colors import ColorScheme


class FinanceColorScheme(ColorScheme):
    """
    金融行业配色方案
    """

    def get_primary(self) -> str:
        """主色：金融蓝"""
        return '#1e40af'

    def get_secondary(self) -> str:
        """辅助色：科技蓝"""
        return '#3b82f6'

    def get_background(self) -> str:
        """背景色：极浅蓝"""
        return '#eff6ff'

    def get_dark_background(self) -> str:
        """深色背景：深蓝黑"""
        return '#0f172a'

    def get_gradient(self, steps: int = 5) -> List[str]:
        """
        金融蓝渐变

        从深蓝到浅蓝的渐变序列
        """
        gradient = [
            '#1e3a8a',  # 深蓝
            '#1e40af',  # 标准金融蓝
            '#2563eb',
            '#3b82f6',  # 科技蓝
            '#60a5fa',
            '#93c5fd',
            '#dbeafe'   # 极浅蓝
        ]

        if steps <= len(gradient):
            step_size = len(gradient) / steps
            return [gradient[int(i * step_size)] for i in range(steps)]
        else:
            return gradient

    def get_categorical(self, n: int = 5) -> List[str]:
        """
        金融主题分类配色

        以金融蓝为主，搭配专业色系
        """
        colors = [
            '#1e40af',  # 金融蓝（主色）
            '#3b82f6',  # 科技蓝（辅助）
            '#10b981',  # 绿色（增长）
            '#f59e0b',  # 金色（财富）
            '#ef4444',  # 红色（风险）
            '#8b5cf6',  # 紫色（高端）
            '#06b6d4',  # 青色（流动性）
            '#64748b'   # 灰蓝（稳健）
        ]
        return colors[:n]

    def get_positive_color(self) -> str:
        """正向指标颜色（盈利/增长）"""
        return '#10b981'  # 绿色

    def get_negative_color(self) -> str:
        """负向指标颜色（亏损/下跌）"""
        return '#ef4444'  # 红色

    def get_neutral_color(self) -> str:
        """中性指标颜色"""
        return '#64748b'  # 灰蓝色

    def get_gold_accent(self) -> str:
        """金色强调（财富/高端）"""
        return '#f59e0b'


def main():
    """测试金融配色方案"""
    print("="*60)
    print("测试: 金融行业配色方案")
    print("="*60)

    scheme = FinanceColorScheme()

    print(f"\n主色: {scheme.get_primary()}")
    print(f"辅助色: {scheme.get_secondary()}")
    print(f"背景色: {scheme.get_background()}")
    print(f"深色背景: {scheme.get_dark_background()}")

    print(f"\n渐变色（5步）:")
    for i, color in enumerate(scheme.get_gradient(5), 1):
        print(f"  {i}. {color}")

    print(f"\n分类色（5个）:")
    for i, color in enumerate(scheme.get_categorical(5), 1):
        print(f"  {i}. {color}")

    print(f"\n特殊用途:")
    print(f"  正向: {scheme.get_positive_color()}")
    print(f"  负向: {scheme.get_negative_color()}")
    print(f"  中性: {scheme.get_neutral_color()}")
    print(f"  金色强调: {scheme.get_gold_accent()}")


if __name__ == '__main__':
    main()
