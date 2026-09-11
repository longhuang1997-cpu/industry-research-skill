"""
雷达图生成器

用于展示多维度对比分析:
- PEST分析（4个维度）
- 波特五力（5个维度）
- 竞争力对比

数据格式示例:
{
    'title': 'PEST分析雷达图',
    'dimensions': ['Political', 'Economic', 'Social', 'Technological'],
    'series': [
        {
            'name': '当前状态',
            'values': [8, 6, 7, 5]
        }
    ],
    'max_value': 10
}
"""

import sys
from pathlib import Path
from typing import Dict, List
import math

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from execution.charts.chart_base import ChartBase


class RadarChart(ChartBase):
    """
    雷达图生成器

    展示多维度数据的对比分析
    """

    def __init__(self,
                 title: str,
                 industry: str = 'default',
                 width: int = 1920,
                 height: int = 1080):
        """
        初始化雷达图

        Args:
            title: 图表标题
            industry: 行业类型
            width: 图表宽度
            height: 图表高度
        """
        super().__init__(title, industry, width, height)

    def generate(self, data: Dict) -> str:
        """
        生成雷达图SVG

        Args:
            data: 图表数据
                {
                    'dimensions': ['维度1', '维度2', ...],
                    'series': [
                        {
                            'name': '系列名称',
                            'values': [值1, 值2, ...]
                        }
                    ],
                    'max_value': 最大值
                }

        Returns:
            svg: SVG字符串
        """
        dimensions = data.get('dimensions', [])
        series = data.get('series', [])
        max_value = data.get('max_value', 10)

        if not dimensions or not series:
            raise ValueError("雷达图数据不能为空")

        # 开始生成SVG
        svg = self._create_svg_header()
        svg += self._add_background()

        # 添加标题
        svg += self._add_title(self.width // 2, 120, font_size=56)

        # 计算绘图区域
        center_x = self.width // 2
        center_y = self.height // 2
        radius = min(self.width, self.height) // 3

        # 计算维度数量
        n_dimensions = len(dimensions)

        # 辅助函数：计算极坐标位置
        def polar_to_cartesian(angle_deg, r):
            """将极坐标转换为笛卡尔坐标"""
            angle_rad = math.radians(angle_deg - 90)  # 从12点方向开始
            x = center_x + r * math.cos(angle_rad)
            y = center_y + r * math.sin(angle_rad)
            return int(x), int(y)

        # 绘制网格圆圈（5个层级）
        n_levels = 5
        for i in range(1, n_levels + 1):
            r = radius * i / n_levels
            svg += self._add_circle(
                center_x, center_y, int(r),
                fill='none',
                stroke='#e5e7eb',
                stroke_width=1
            )

        # 绘制维度轴线
        angle_step = 360 / n_dimensions

        for i in range(n_dimensions):
            angle = i * angle_step
            x, y = polar_to_cartesian(angle, radius)

            # 轴线
            svg += self._add_line(
                center_x, center_y,
                x, y,
                stroke='#9ca3af',
                stroke_width=2
            )

            # 维度标签
            label_x, label_y = polar_to_cartesian(angle, radius + 80)
            svg += self._add_text(
                label_x, label_y,
                dimensions[i],
                font_size=24,
                color='#374151',
                anchor='middle',
                weight='bold'
            )

        # 绘制系列数据
        colors = self.colors.get_categorical(len(series))

        for idx, s in enumerate(series):
            series_name = s['name']
            series_values = s['values']
            series_color = colors[idx % len(colors)]

            if len(series_values) != n_dimensions:
                continue

            # 构建多边形路径
            points = []
            for i in range(n_dimensions):
                angle = i * angle_step
                value = series_values[i]
                r = radius * (value / max_value)
                x, y = polar_to_cartesian(angle, r)
                points.append(f"{x},{y}")

            # 绘制填充多边形
            svg += f'<polygon points="{" ".join(points)}" '
            svg += f'fill="{series_color}" fill-opacity="0.2" '
            svg += f'stroke="{series_color}" stroke-width="3" />\n'

            # 绘制数据点
            for i in range(n_dimensions):
                angle = i * angle_step
                value = series_values[i]
                r = radius * (value / max_value)
                x, y = polar_to_cartesian(angle, r)

                svg += self._add_circle(
                    x, y, 6,
                    fill=series_color,
                    stroke='#ffffff',
                    stroke_width=2
                )

        # 添加图例
        legend_x = 200
        legend_y = self.height - 200

        for idx, s in enumerate(series):
            series_name = s['name']
            series_color = colors[idx % len(colors)]

            # 图例矩形
            svg += self._add_rect(
                legend_x, legend_y + idx * 40,
                30, 20,
                fill=series_color
            )

            # 图例文字
            svg += self._add_text(
                legend_x + 40,
                legend_y + idx * 40 + 15,
                series_name,
                font_size=22,
                color='#374151'
            )

        svg += self._create_svg_footer()
        return svg


def main():
    """测试雷达图生成器"""
    print("="*60)
    print("Test: Radar Chart Generator")
    print("="*60)

    # 测试数据：PEST分析
    test_data = {
        'dimensions': ['Political', 'Economic', 'Social', 'Technological'],
        'series': [
            {
                'name': '当前影响',
                'values': [8, 6, 7, 5]
            },
            {
                'name': '未来预期',
                'values': [9, 7, 8, 7]
            }
        ],
        'max_value': 10
    }

    # 生成图表
    chart = RadarChart(
        'PEST分析雷达图',
        industry='medical'
    )

    output_path = Path('./output/test_radar_chart.svg')
    chart.save(test_data, output_path)

    print(f"\n[OK] Radar chart generated: {output_path}")
    print(f"Dimensions: {len(test_data['dimensions'])}")
    print(f"Series: {len(test_data['series'])}")


if __name__ == '__main__':
    main()
