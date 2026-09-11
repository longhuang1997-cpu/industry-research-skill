"""
医疗健康行业配色方案

配色理念:
- 主色：医疗绿（#059669）- 专业、信任、生命力
- 辅助色：浅绿（#10b981, #ecfdf5）- 舒适、健康
- 适用场景：医疗陪护、养老服务、健康管理
"""

from typing import List
from .colors import ColorScheme


class MedicalColorScheme(ColorScheme):
    """
    医疗健康行业配色方案
    """

    def get_primary(self) -> str:
        """主色：医疗绿"""
        return '#059669'

    def get_secondary(self) -> str:
        """辅助色：浅绿"""
        return '#10b981'

    def get_background(self) -> str:
        """背景色：极浅绿"""
        return '#ecfdf5'

    def get_gradient(self, steps: int = 5) -> List[str]:
        """
        医疗绿渐变

        从深绿到浅绿的渐变序列
        """
        gradient = [
            '#065f46',  # 深绿
            '#047857',
            '#059669',  # 标准医疗绿
            '#10b981',
            '#34d399',
            '#6ee7b7',
            '#a7f3d0'   # 极浅绿
        ]

        # 根据需要的步数选择均匀分布的颜色
        if steps <= len(gradient):
            step_size = len(gradient) / steps
            return [gradient[int(i * step_size)] for i in range(steps)]
        else:
            return gradient

    def get_categorical(self, n: int = 5) -> List[str]:
        """
        医疗主题分类配色

        以医疗绿为主，搭配互补色
        """
        colors = [
            '#059669',  # 医疗绿（主色）
            '#10b981',  # 浅绿（辅助）
            '#3b82f6',  # 蓝色（科技感）
            '#f59e0b',  # 橙色（警示）
            '#ef4444',  # 红色（紧急）
            '#8b5cf6',  # 紫色（高端）
            '#06b6d4',  # 青色（清新）
            '#84cc16'   # 黄绿（活力）
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


def main():
    """测试医疗配色方案"""
    print("="*60)
    print("测试: 医疗健康配色方案")
    print("="*60)

    scheme = MedicalColorScheme()

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


if __name__ == '__main__':
    main()
