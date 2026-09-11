"""
瀑布图生成器

用于展示单位经济模型的现金流变化:
- 从收入开始
- 逐步扣减各项成本
- 最终得到利润

数据格式示例:
{
    'items': [
        {'label': '单位收入', 'value': 500, 'type': 'start'},
        {'label': '人力成本', 'value': -200, 'type': 'decrease'},
        {'label': '材料成本', 'value': -100, 'type': 'decrease'},
        {'label': '运营成本', 'value': -50, 'type': 'decrease'},
        {'label': '单位利润', 'value': 150, 'type': 'end'}
    ],
    'unit': '元'
}
"""

import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from execution.charts.chart_base import ChartBase


class WaterfallChart(ChartBase):
    """
    瀑布图生成器

    展示单位经济模型的现金流瀑布效果
    """

    def __init__(self,
                 title: str,
                 industry: str = 'default',
                 width: int = 1920,
                 height: int = 1080):
        """
        初始化瀑布图

        Args:
            title: 图表标题
            industry: 行业类型
            width: 图表宽度
            height: 图表高度
        """
        super().__init__(title, industry, width, height)

    def generate(self, data: Dict) -> str:
        """
        生成瀑布图SVG

        Args:
            data: 图表数据
                {
                    'items': [
                        {'label': '项目名', 'value': 数值, 'type': 'start/increase/decrease/end'},
                        ...
                    ],
                    'unit': '单位'
                }

        Returns:
            svg: SVG字符串
        """
        items = data.get('items', [])
        unit = data.get('unit', '')

        if not items:
            raise ValueError("瀑布图数据不能为空")

        # 开始生成SVG
        svg = self._create_svg_header()
        svg += self._add_background()

        # 添加标题
        svg += self._add_title(self.width // 2, 120, font_size=56)

        # 计算绘图区域
        chart_left = 200
        chart_width = self.width - 400
        chart_top = 250
        chart_height = 650

        # 计算每个柱子的宽度和间距
        bar_count = len(items)
        bar_spacing = 60
        bar_width = (chart_width - (bar_count - 1) * bar_spacing) / bar_count

        # 找出最大值用于缩放
        max_value = max(abs(item['value']) for item in items)
        max_cumulative = 0
        cumulative = 0
        for item in items:
            cumulative += item['value']
            max_cumulative = max(max_cumulative, abs(cumulative))

        scale_max = max(max_value, max_cumulative) * 1.2  # 留20%余量

        # 辅助函数：值转换为Y坐标
        def value_to_y(value):
            return chart_top + chart_height - (value / scale_max * chart_height)

        # 绘制Y轴和刻度
        svg += self._add_line(
            chart_left - 50, chart_top,
            chart_left - 50, chart_top + chart_height,
            stroke='#9ca3af',
            stroke_width=2
        )

        # Y轴刻度（5个刻度）
        for i in range(6):
            tick_value = scale_max * i / 5
            tick_y = value_to_y(tick_value)
            svg += self._add_line(
                chart_left - 60, tick_y,
                chart_left - 40, tick_y,
                stroke='#9ca3af',
                stroke_width=2
            )
            svg += self._add_text(
                chart_left - 70,
                tick_y + 5,
                f"{int(tick_value)}",
                font_size=20,
                color='#6b7280',
                anchor='end'
            )

        # 零线
        zero_y = value_to_y(0)
        svg += self._add_line(
            chart_left - 50, zero_y,
            chart_left + chart_width, zero_y,
            stroke='#374151',
            stroke_width=2
        )

        # 绘制瀑布柱
        cumulative_value = 0
        positive_color = self.colors.get_positive_color()
        negative_color = self.colors.get_negative_color()
        primary_color = self.colors.get_primary()

        for i, item in enumerate(items):
            label = item['label']
            value = item['value']
            item_type = item.get('type', 'normal')

            # 计算X位置
            bar_x = chart_left + i * (bar_width + bar_spacing)
            bar_center_x = bar_x + bar_width / 2

            # 根据类型选择颜色
            if item_type in ['start', 'end']:
                bar_color = primary_color
            elif value > 0:
                bar_color = positive_color
            else:
                bar_color = negative_color

            # 计算柱子高度和位置
            if item_type == 'start':
                # 起始柱：从0开始
                bar_bottom_y = zero_y
                bar_top_y = value_to_y(value)
                bar_height = abs(bar_bottom_y - bar_top_y)

                # 绘制柱子
                svg += self._add_rect(
                    int(bar_x), int(bar_top_y),
                    int(bar_width), int(bar_height),
                    fill=bar_color,
                    stroke='#ffffff',
                    stroke_width=3
                )

                cumulative_value = value

            elif item_type == 'end':
                # 结束柱：显示累积值
                bar_bottom_y = zero_y
                bar_top_y = value_to_y(cumulative_value)
                bar_height = abs(bar_bottom_y - bar_top_y)

                # 绘制柱子
                svg += self._add_rect(
                    int(bar_x), int(bar_top_y),
                    int(bar_width), int(bar_height),
                    fill=bar_color,
                    stroke='#ffffff',
                    stroke_width=3
                )

            else:
                # 中间柱：增量或减量
                prev_cumulative = cumulative_value
                cumulative_value += value

                if value > 0:
                    # 增量：向上
                    bar_bottom_y = value_to_y(prev_cumulative)
                    bar_top_y = value_to_y(cumulative_value)
                else:
                    # 减量：向下
                    bar_top_y = value_to_y(cumulative_value)
                    bar_bottom_y = value_to_y(prev_cumulative)

                bar_height = abs(bar_bottom_y - bar_top_y)

                # 绘制柱子
                svg += self._add_rect(
                    int(bar_x), int(bar_top_y),
                    int(bar_width), int(bar_height),
                    fill=bar_color,
                    stroke='#ffffff',
                    stroke_width=3
                )

                # 连接线（虚线）
                if i > 0:
                    prev_bar_x = chart_left + (i - 1) * (bar_width + bar_spacing)
                    prev_bar_right = prev_bar_x + bar_width
                    svg += self._add_line(
                        int(prev_bar_right), int(value_to_y(prev_cumulative)),
                        int(bar_x), int(value_to_y(prev_cumulative)),
                        stroke='#9ca3af',
                        stroke_width=2,
                        dash_array='5,5'
                    )

            # 添加标签
            svg += self._add_text(
                int(bar_center_x),
                chart_top + chart_height + 40,
                label,
                font_size=24,
                color='#374151',
                anchor='middle',
                weight='normal'
            )

            # 添加数值标签
            value_y = bar_top_y - 20 if value >= 0 else bar_bottom_y + 35
            value_text = f"{value:+.0f}" if item_type not in ['start', 'end'] else f"{abs(value):.0f}"
            svg += self._add_text(
                int(bar_center_x),
                int(value_y),
                value_text,
                font_size=28,
                color='#1f2937',
                anchor='middle',
                weight='bold'
            )

        # 添加单位说明
        if unit:
            svg += self._add_text(
                self.width // 2,
                self.height - 50,
                f"单位: {unit}",
                font_size=28,
                color='#6b7280',
                anchor='middle'
            )

        svg += self._create_svg_footer()
        return svg


def main():
    """测试瀑布图生成器"""
    print("="*60)
    print("Test: Waterfall Chart Generator")
    print("="*60)

    # 测试数据：单位经济模型
    test_data = {
        'items': [
            {'label': '单位收入', 'value': 500, 'type': 'start'},
            {'label': '人力成本', 'value': -200, 'type': 'decrease'},
            {'label': '材料成本', 'value': -100, 'type': 'decrease'},
            {'label': '运营成本', 'value': -50, 'type': 'decrease'},
            {'label': '营销费用', 'value': -30, 'type': 'decrease'},
            {'label': '单位毛利', 'value': 120, 'type': 'end'}
        ],
        'unit': '元/单位'
    }

    # 生成图表
    chart = WaterfallChart(
        '医疗陪护单位经济模型',
        industry='medical'
    )

    output_path = Path('./output/test_waterfall_chart.svg')
    chart.save(test_data, output_path)

    print(f"\n[OK] Waterfall chart generated: {output_path}")
    print(f"Items: {len(test_data['items'])}")


if __name__ == '__main__':
    main()
