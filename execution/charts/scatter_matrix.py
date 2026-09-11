"""
散点矩阵图生成器

用于展示竞争格局:
- 四象限坐标系
- 企业定位散点
- 标签和气泡

数据格式示例:
{
    'competitors': [
        {'name': '企业A', 'x': 8.5, 'y': 7.2, 'size': 100},
        {'name': '企业B', 'x': 6.3, 'y': 8.1, 'size': 80},
        ...
    ],
    'x_label': '市场份额 (%)',
    'y_label': '增长率 (%)',
    'quadrants': ['问题', '明星', '瘦狗', '金牛']
}
"""

import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from execution.charts.chart_base import ChartBase


class ScatterMatrixChart(ChartBase):
    """
    散点矩阵图生成器

    展示竞争格局的四象限分布
    """

    def __init__(self,
                 title: str,
                 industry: str = 'default',
                 width: int = 1920,
                 height: int = 1080):
        """
        初始化散点矩阵图

        Args:
            title: 图表标题
            industry: 行业类型
            width: 图表宽度
            height: 图表高度
        """
        super().__init__(title, industry, width, height)

    def generate(self, data: Dict) -> str:
        """
        生成散点矩阵图SVG

        Args:
            data: 图表数据
                {
                    'competitors': [
                        {'name': '企业名', 'x': X值, 'y': Y值, 'size': 大小},
                        ...
                    ],
                    'x_label': 'X轴标签',
                    'y_label': 'Y轴标签',
                    'quadrants': ['左下', '右下', '左上', '右上']  # 可选
                }

        Returns:
            svg: SVG字符串
        """
        competitors = data.get('competitors', [])
        x_label = data.get('x_label', 'X轴')
        y_label = data.get('y_label', 'Y轴')
        quadrants = data.get('quadrants', ['Q3', 'Q4', 'Q2', 'Q1'])

        if not competitors:
            raise ValueError("散点矩阵图数据不能为空")

        # 开始生成SVG
        svg = self._create_svg_header()
        svg += self._add_background()

        # 添加标题
        svg += self._add_title(self.width // 2, 120, font_size=56)

        # 计算绘图区域
        chart_left = 250
        chart_width = self.width - 500
        chart_top = 250
        chart_height = self.height - 450

        # 坐标轴中心点
        center_x = chart_left + chart_width // 2
        center_y = chart_top + chart_height // 2

        # 获取数据范围
        x_values = [c['x'] for c in competitors]
        y_values = [c['y'] for c in competitors]

        x_min, x_max = min(x_values), max(x_values)
        y_min, y_max = min(y_values), max(y_values)

        # 扩展范围10%
        x_range = x_max - x_min
        y_range = y_max - y_min
        x_min -= x_range * 0.1
        x_max += x_range * 0.1
        y_min -= y_range * 0.1
        y_max += y_range * 0.1

        # 辅助函数：值转换为坐标
        def value_to_x(value):
            if x_max == x_min:
                return center_x
            return chart_left + ((value - x_min) / (x_max - x_min)) * chart_width

        def value_to_y(value):
            if y_max == y_min:
                return center_y
            return chart_top + chart_height - ((value - y_min) / (y_max - y_min)) * chart_height

        # 绘制四象限背景
        quadrant_colors = [
            self.colors.get_background(),
            '#f9fafb',
            '#f3f4f6',
            '#e5e7eb'
        ]

        # 左下象限
        svg += self._add_rect(
            chart_left, center_y,
            chart_width // 2, chart_height // 2,
            fill=quadrant_colors[0],
            stroke='#d1d5db',
            stroke_width=1
        )

        # 右下象限
        svg += self._add_rect(
            center_x, center_y,
            chart_width // 2, chart_height // 2,
            fill=quadrant_colors[1],
            stroke='#d1d5db',
            stroke_width=1
        )

        # 左上象限
        svg += self._add_rect(
            chart_left, chart_top,
            chart_width // 2, chart_height // 2,
            fill=quadrant_colors[2],
            stroke='#d1d5db',
            stroke_width=1
        )

        # 右上象限
        svg += self._add_rect(
            center_x, chart_top,
            chart_width // 2, chart_height // 2,
            fill=quadrant_colors[3],
            stroke='#d1d5db',
            stroke_width=1
        )

        # 添加象限标签
        svg += self._add_text(
            chart_left + chart_width // 4,
            center_y + chart_height // 4,
            quadrants[0],
            font_size=32,
            color='#9ca3af',
            anchor='middle',
            weight='bold'
        )

        svg += self._add_text(
            center_x + chart_width // 4,
            center_y + chart_height // 4,
            quadrants[1],
            font_size=32,
            color='#9ca3af',
            anchor='middle',
            weight='bold'
        )

        svg += self._add_text(
            chart_left + chart_width // 4,
            chart_top + chart_height // 4,
            quadrants[2],
            font_size=32,
            color='#9ca3af',
            anchor='middle',
            weight='bold'
        )

        svg += self._add_text(
            center_x + chart_width // 4,
            chart_top + chart_height // 4,
            quadrants[3],
            font_size=32,
            color='#9ca3af',
            anchor='middle',
            weight='bold'
        )

        # 绘制坐标轴
        primary_color = self.colors.get_primary()

        # X轴
        svg += self._add_line(
            chart_left, center_y,
            chart_left + chart_width, center_y,
            stroke=primary_color,
            stroke_width=3
        )

        # Y轴
        svg += self._add_line(
            center_x, chart_top,
            center_x, chart_top + chart_height,
            stroke=primary_color,
            stroke_width=3
        )

        # X轴刻度和标签
        for i in range(5):
            x_value = x_min + (x_max - x_min) * i / 4
            x_pos = value_to_x(x_value)

            # 刻度线
            svg += self._add_line(
                int(x_pos), center_y - 8,
                int(x_pos), center_y + 8,
                stroke='#6b7280',
                stroke_width=2
            )

            # 标签
            svg += self._add_text(
                int(x_pos),
                center_y + 35,
                f'{x_value:.1f}',
                font_size=20,
                color='#6b7280',
                anchor='middle'
            )

        # Y轴刻度和标签
        for i in range(5):
            y_value = y_min + (y_max - y_min) * i / 4
            y_pos = value_to_y(y_value)

            # 刻度线
            svg += self._add_line(
                center_x - 8, int(y_pos),
                center_x + 8, int(y_pos),
                stroke='#6b7280',
                stroke_width=2
            )

            # 标签
            svg += self._add_text(
                center_x - 20,
                int(y_pos) + 5,
                f'{y_value:.1f}',
                font_size=20,
                color='#6b7280',
                anchor='end'
            )

        # 轴标签
        svg += self._add_text(
            chart_left + chart_width // 2,
            chart_top + chart_height + 80,
            x_label,
            font_size=28,
            color='#374151',
            anchor='middle',
            weight='bold'
        )

        svg += self._add_text(
            chart_left - 120,
            chart_top + chart_height // 2,
            y_label,
            font_size=28,
            color='#374151',
            anchor='middle',
            weight='bold'
        )

        # 绘制散点
        colors = self.colors.get_categorical(len(competitors))

        for i, competitor in enumerate(competitors):
            name = competitor['name']
            x = competitor['x']
            y = competitor['y']
            size = competitor.get('size', 50)

            # 计算位置
            cx = value_to_x(x)
            cy = value_to_y(y)

            # 气泡半径（基于size）
            radius = int(size * 0.5)  # 缩放因子

            # 绘制气泡
            bubble_color = colors[i % len(colors)]
            svg += self._add_circle(
                int(cx), int(cy),
                radius,
                fill=bubble_color,
                stroke='#ffffff',
                stroke_width=3
            )

            # 添加企业名称
            svg += self._add_text(
                int(cx),
                int(cy) + 5,
                name,
                font_size=20,
                color='#ffffff',
                anchor='middle',
                weight='bold'
            )

            # 添加数值标签（在气泡外）
            label_y = cy - radius - 15
            svg += self._add_text(
                int(cx),
                int(label_y),
                f'({x:.1f}, {y:.1f})',
                font_size=18,
                color='#6b7280',
                anchor='middle'
            )

        svg += self._create_svg_footer()
        return svg


def main():
    """测试散点矩阵图生成器"""
    print("="*60)
    print("Test: Scatter Matrix Chart Generator")
    print("="*60)

    # 测试数据：竞争格局分析
    test_data = {
        'competitors': [
            {'name': '爱康国宾', 'x': 8.5, 'y': 7.2, 'size': 120},
            {'name': '美年健康', 'x': 7.8, 'y': 6.5, 'size': 100},
            {'name': '瑞慈医疗', 'x': 4.2, 'y': 8.1, 'size': 60},
            {'name': '慈铭体检', 'x': 5.5, 'y': 3.8, 'size': 70},
            {'name': '新进入者A', 'x': 2.1, 'y': 9.5, 'size': 30},
            {'name': '区域企业B', 'x': 3.5, 'y': 2.2, 'size': 40}
        ],
        'x_label': '市场份额 (%)',
        'y_label': '增长率 (%)',
        'quadrants': ['低份额低增长', '高份额低增长', '低份额高增长', '高份额高增长']
    }

    # 生成图表
    chart = ScatterMatrixChart(
        '医疗陪护企业竞争格局（2024）',
        industry='medical'
    )

    output_path = Path('./output/test_scatter_matrix_chart.svg')
    chart.save(test_data, output_path)

    print(f"\n[OK] Scatter matrix chart generated: {output_path}")
    print(f"Competitors: {len(test_data['competitors'])}")


if __name__ == '__main__':
    main()
