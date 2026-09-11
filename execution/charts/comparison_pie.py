"""
对比饼图生成器

用于展示支付结构对比:
- 两个饼图并排对比
- 展示不同维度的占比差异
- 适用场景：自费vs保险、B端vs C端等

数据格式示例:
{
    'left': {
        'title': '当前支付结构',
        'data': {'自费': 70, '保险': 20, '政府': 10}
    },
    'right': {
        'title': '目标支付结构',
        'data': {'自费': 40, '保险': 40, '政府': 20}
    }
}
"""

import sys
import math
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from execution.charts.chart_base import ChartBase


class ComparisonPieChart(ChartBase):
    """
    对比饼图生成器

    展示两个饼图的对比分析
    """

    def __init__(self,
                 title: str,
                 industry: str = 'default',
                 width: int = 1920,
                 height: int = 1080):
        """
        初始化对比饼图

        Args:
            title: 图表标题
            industry: 行业类型
            width: 图表宽度
            height: 图表高度
        """
        super().__init__(title, industry, width, height)

    def generate(self, data: Dict) -> str:
        """
        生成对比饼图SVG

        Args:
            data: 图表数据
                {
                    'left': {'title': '左侧标题', 'data': {'项目1': 值1, ...}},
                    'right': {'title': '右侧标题', 'data': {'项目2': 值2, ...}}
                }

        Returns:
            svg: SVG字符串
        """
        left_chart = data.get('left', {})
        right_chart = data.get('right', {})

        if not left_chart or not right_chart:
            raise ValueError("对比饼图需要左右两组数据")

        # 开始生成SVG
        svg = self._create_svg_header()
        svg += self._add_background()

        # 添加标题
        svg += self._add_title(self.width // 2, 120, font_size=56)

        # 获取分类配色（确保两边用相同的颜色对应相同的项目）
        all_items = set(left_chart['data'].keys()) | set(right_chart['data'].keys())
        color_map = {}
        colors = self.colors.get_categorical(len(all_items))
        for i, item in enumerate(sorted(all_items)):
            color_map[item] = colors[i % len(colors)]

        # 绘制左侧饼图
        left_center_x = self.width // 4
        center_y = self.height // 2
        radius = 250

        svg += self._draw_pie_chart(
            left_chart['title'],
            left_chart['data'],
            left_center_x,
            center_y,
            radius,
            color_map
        )

        # 绘制右侧饼图
        right_center_x = self.width * 3 // 4
        svg += self._draw_pie_chart(
            right_chart['title'],
            right_chart['data'],
            right_center_x,
            center_y,
            radius,
            color_map
        )

        # 添加图例（底部居中）
        legend_items = [{'label': k, 'color': v} for k, v in color_map.items()]
        svg += self._add_legend(
            legend_items,
            self.width // 2 - len(legend_items) * 100,
            self.height - 80,
            item_width=200
        )

        svg += self._create_svg_footer()
        return svg

    def _draw_pie_chart(self,
                       title: str,
                       data: Dict,
                       center_x: int,
                       center_y: int,
                       radius: int,
                       color_map: Dict) -> str:
        """
        绘制单个饼图

        Args:
            title: 饼图标题
            data: 数据 {'项目': 值, ...}
            center_x: 圆心X坐标
            center_y: 圆心Y坐标
            radius: 半径
            color_map: 颜色映射

        Returns:
            svg: SVG片段
        """
        svg = ''

        # 添加小标题
        svg += self._add_text(
            center_x,
            center_y - radius - 50,
            title,
            font_size=36,
            color='#1f2937',
            anchor='middle',
            weight='bold'
        )

        # 计算总值
        total = sum(data.values())
        if total == 0:
            return svg

        # 绘制饼图扇形
        start_angle = 0

        for label, value in data.items():
            percentage = value / total
            angle = percentage * 360

            # 计算扇形路径
            end_angle = start_angle + angle

            # 转换为弧度
            start_rad = math.radians(start_angle - 90)  # -90度使其从顶部开始
            end_rad = math.radians(end_angle - 90)

            # 计算起点和终点
            start_x = center_x + radius * math.cos(start_rad)
            start_y = center_y + radius * math.sin(start_rad)
            end_x = center_x + radius * math.cos(end_rad)
            end_y = center_y + radius * math.sin(end_rad)

            # 大弧标志
            large_arc_flag = 1 if angle > 180 else 0

            # 绘制扇形路径
            path_d = f'M {center_x},{center_y} L {start_x},{start_y} A {radius},{radius} 0 {large_arc_flag},1 {end_x},{end_y} Z'

            color = color_map.get(label, '#cccccc')
            svg += self._add_path(
                path_d,
                fill=color,
                stroke='#ffffff',
                stroke_width=3
            )

            # 添加百分比标签（在扇形中间）
            if percentage > 0.05:  # 只在大于5%时显示
                mid_angle = start_angle + angle / 2
                mid_rad = math.radians(mid_angle - 90)
                label_radius = radius * 0.65

                label_x = center_x + label_radius * math.cos(mid_rad)
                label_y = center_y + label_radius * math.sin(mid_rad)

                svg += self._add_text(
                    int(label_x),
                    int(label_y),
                    f'{percentage * 100:.1f}%',
                    font_size=24,
                    color='#ffffff',
                    anchor='middle',
                    weight='bold'
                )

            start_angle = end_angle

        return svg


def main():
    """测试对比饼图生成器"""
    print("="*60)
    print("Test: Comparison Pie Chart Generator")
    print("="*60)

    # 测试数据：支付结构对比
    test_data = {
        'left': {
            'title': '当前支付结构（2024）',
            'data': {
                '自费': 70,
                '商业保险': 20,
                '政府补贴': 10
            }
        },
        'right': {
            'title': '目标支付结构（2030）',
            'data': {
                '自费': 40,
                '商业保险': 35,
                '长护险': 15,
                '政府补贴': 10
            }
        }
    }

    # 生成图表
    chart = ComparisonPieChart(
        '医疗陪护支付结构演进对比',
        industry='medical'
    )

    output_path = Path('./output/test_comparison_pie_chart.svg')
    chart.save(test_data, output_path)

    print(f"\n[OK] Comparison pie chart generated: {output_path}")
    print(f"Left items: {len(test_data['left']['data'])}")
    print(f"Right items: {len(test_data['right']['data'])}")


if __name__ == '__main__':
    main()
