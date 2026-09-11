"""
趋势图生成器

用于展示时间序列数据:
- 市场规模趋势
- 增长率变化
- 多指标对比

数据格式示例:
{
    'title': '市场规模趋势（2015-2025）',
    'series': [
        {
            'name': '市场规模',
            'data': [
                {'year': 2015, 'value': 100},
                {'year': 2016, 'value': 150},
                ...
            ]
        }
    ],
    'y_label': '市场规模（亿元）',
    'show_markers': True
}
"""

import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from execution.charts.chart_base import ChartBase


class LineChart(ChartBase):
    """
    趋势图生成器

    展示时间序列数据的变化趋势
    """

    def __init__(self,
                 title: str,
                 industry: str = 'default',
                 width: int = 1920,
                 height: int = 1080):
        """
        初始化趋势图

        Args:
            title: 图表标题
            industry: 行业类型
            width: 图表宽度
            height: 图表高度
        """
        super().__init__(title, industry, width, height)

    def generate(self, data: Dict) -> str:
        """
        生成趋势图SVG

        Args:
            data: 图表数据
                {
                    'series': [
                        {
                            'name': '系列名称',
                            'data': [{'year': 年份, 'value': 值}, ...]
                        }
                    ],
                    'y_label': 'Y轴标签',
                    'show_markers': True/False
                }

        Returns:
            svg: SVG字符串
        """
        series = data.get('series', [])
        y_label = data.get('y_label', 'Value')
        show_markers = data.get('show_markers', True)

        if not series:
            raise ValueError("趋势图数据不能为空")

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

        # 获取所有数据点
        all_years = []
        all_values = []
        for s in series:
            for point in s['data']:
                all_years.append(point['year'])
                all_values.append(point['value'])

        if not all_years:
            raise ValueError("系列数据为空")

        year_min = min(all_years)
        year_max = max(all_years)
        value_min = min(all_values)
        value_max = max(all_values)

        # 扩展Y轴范围10%
        value_range = value_max - value_min
        if value_range == 0:
            value_range = value_max * 0.1 if value_max != 0 else 1
        value_min = max(0, value_min - value_range * 0.1)
        value_max = value_max + value_range * 0.1

        # 辅助函数：值转换为坐标
        def year_to_x(year):
            if year_max == year_min:
                return chart_left + chart_width // 2
            return chart_left + ((year - year_min) / (year_max - year_min)) * chart_width

        def value_to_y(value):
            if value_max == value_min:
                return chart_top + chart_height // 2
            return chart_top + chart_height - ((value - value_min) / (value_max - value_min)) * chart_height

        # 绘制坐标轴
        primary_color = self.colors.get_primary()

        # X轴
        svg += self._add_line(
            chart_left, chart_top + chart_height,
            chart_left + chart_width, chart_top + chart_height,
            stroke='#6b7280',
            stroke_width=2
        )

        # Y轴
        svg += self._add_line(
            chart_left, chart_top,
            chart_left, chart_top + chart_height,
            stroke='#6b7280',
            stroke_width=2
        )

        # X轴刻度（年份）
        year_step = max(1, (year_max - year_min) // 10)
        for year in range(year_min, year_max + 1, year_step):
            x_pos = year_to_x(year)
            svg += self._add_line(
                int(x_pos), chart_top + chart_height - 8,
                int(x_pos), chart_top + chart_height + 8,
                stroke='#6b7280',
                stroke_width=2
            )
            svg += self._add_text(
                int(x_pos),
                chart_top + chart_height + 35,
                str(year),
                font_size=20,
                color='#6b7280',
                anchor='middle'
            )

        # Y轴刻度
        y_tick_count = 5
        for i in range(y_tick_count + 1):
            value = value_min + (value_max - value_min) * i / y_tick_count
            y_pos = value_to_y(value)

            # 刻度线
            svg += self._add_line(
                chart_left - 8, int(y_pos),
                chart_left + 8, int(y_pos),
                stroke='#6b7280',
                stroke_width=2
            )

            # 网格线
            svg += self._add_line(
                chart_left, int(y_pos),
                chart_left + chart_width, int(y_pos),
                stroke='#e5e7eb',
                stroke_width=1
            )

            # 标签
            svg += self._add_text(
                chart_left - 20,
                int(y_pos) + 5,
                f'{value:.0f}',
                font_size=20,
                color='#6b7280',
                anchor='end'
            )

        # Y轴标签
        svg += self._add_text(
            chart_left - 120,
            chart_top + chart_height // 2,
            y_label,
            font_size=28,
            color='#374151',
            anchor='middle',
            weight='bold'
        )

        # 绘制系列
        colors = self.colors.get_categorical(len(series))

        for idx, s in enumerate(series):
            series_name = s['name']
            series_data = s['data']
            series_color = colors[idx % len(colors)]

            # 排序数据点
            series_data_sorted = sorted(series_data, key=lambda p: p['year'])

            # 绘制折线
            if len(series_data_sorted) > 1:
                path_points = []
                for point in series_data_sorted:
                    x = year_to_x(point['year'])
                    y = value_to_y(point['value'])
                    path_points.append(f"{int(x)},{int(y)}")

                svg += f'<polyline points="{" ".join(path_points)}" '
                svg += f'fill="none" stroke="{series_color}" stroke-width="3" />\n'

            # 绘制数据点标记
            if show_markers:
                for point in series_data_sorted:
                    x = year_to_x(point['year'])
                    y = value_to_y(point['value'])

                    svg += self._add_circle(
                        int(x), int(y), 6,
                        fill=series_color,
                        stroke='#ffffff',
                        stroke_width=2
                    )

        # 添加图例
        legend_x = chart_left + chart_width - 300
        legend_y = chart_top + 50

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
    """测试趋势图生成器"""
    print("="*60)
    print("Test: Line Chart Generator")
    print("="*60)

    # 测试数据：市场规模趋势
    test_data = {
        'series': [
            {
                'name': '市场规模',
                'data': [
                    {'year': 2015, 'value': 100},
                    {'year': 2016, 'value': 150},
                    {'year': 2017, 'value': 210},
                    {'year': 2018, 'value': 320},
                    {'year': 2019, 'value': 470},
                    {'year': 2020, 'value': 680},
                    {'year': 2021, 'value': 950},
                    {'year': 2022, 'value': 1200},
                    {'year': 2023, 'value': 1480},
                    {'year': 2024, 'value': 1750}
                ]
            }
        ],
        'y_label': '市场规模（亿元）',
        'show_markers': True
    }

    # 生成图表
    chart = LineChart(
        '医疗陪护市场规模趋势（2015-2024）',
        industry='medical'
    )

    output_path = Path('./output/test_line_chart.svg')
    chart.save(test_data, output_path)

    print(f"\n[OK] Line chart generated: {output_path}")
    print(f"Data points: {len(test_data['series'][0]['data'])}")


if __name__ == '__main__':
    main()
