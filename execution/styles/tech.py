"""
科技行业配色方案

配色理念:
- 主色：科技紫（#7c3aed）- 创新、未来感、高科技
- 辅助色：亮紫（#a78bfa）- 活力、想象力
- 背景色：极浅紫（#f3e8ff）- 梦幻、科技
- 适用场景：AI、互联网、SaaS、高科技
"""

from typing import List
from .colors import ColorScheme


class TechColorScheme(ColorScheme):
    """
    科技行业配色方案
    """

    def get_primary(self) -> str:
        """主色：科技紫"""
        return '#7c3aed'

    def get_secondary(self) -> str:
        """辅助色：亮紫"""
        return '#a78bfa'

    def get_background(self) -> str:
        """背景色：极浅紫"""
        return '#f3e8ff'

    def get_gradient(self, steps: int = 5) -> List[str]:
        """
        科技紫渐变

        从深紫到浅紫的渐变序列
        """
        gradient = [
            '#5b21b6',  # 深紫
            '#6d28d9',
            '#7c3aed',  # 标准科技紫
            '#8b5cf6',
            '#a78bfa',  # 亮紫
            '#c4b5fd',
            '#e9d5ff'   # 极浅紫
        ]

        if steps <= len(gradient):
            step_size = len(gradient) / steps
            return [gradient[int(i * step_size)] for i in range(steps)]
        else:
            return gradient

    def get_categorical(self, n: int = 5) -> List[str]:
        """
        科技主题分类配色

        以科技紫为主，搭配现代色系
        """
        colors = [
            '#7c3aed',  # 科技紫（主色）
            '#3b82f6',  # 蓝色（科技）
            '#06b6d4',  # 青色（数据）
            '#10b981',  # 绿色（增长）
            '#f59e0b',  # 橙色（活力）
            '#ec4899',  # 粉色（创新）
            '#8b5cf6',  # 紫色（未来）
            '#14b8a6'   # 青绿（AI）
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

    def get_ai_accent(self) -> str:
        """AI强调色"""
        return '#14b8a6'  # 青绿色

    def get_data_accent(self) -> str:
        """数据强调色"""
        return '#06b6d4'  # 青色


def main():
    """测试科技配色方案"""
    print("="*60)
    print("测试: 科技行业配色方案")
    print("="*60)

    scheme = TechColorScheme()

    print(f"\n主色: {scheme.get_primary()}")
    print(f"辅助色: {scheme.get_secondary()}")
    print(f"背景色: {scheme.get_background()}")

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
    print(f"  AI强调: {scheme.get_ai_accent()}")
    print(f"  数据强调: {scheme.get_data_accent()}")


if __name__ == '__main__':
    main()
