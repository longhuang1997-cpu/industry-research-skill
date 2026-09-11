"""
时间线图生成器

用于展示政策演进或行业发展历程:
- 横向时间轴
- 里程碑标记
- 事件描述

数据格式示例:
{
    'events': [
        {'year': 2015, 'event': '长护险试点启动', 'description': '15个城市试点'},
        {'year': 2018, 'event': '扩大试点范围', 'description': '扩展至49个城市'},
        {'year': 2020, 'event': '全国推广', 'description': '政策全面落地'},
        {'year': 2024, 'event': '覆盖1.8亿人', 'description': '参保人数突破1.8亿'}
    ]
}
"""

import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from execution.charts.chart_base import ChartBase


class TimelineChart(ChartBase):
    """
    时间线图生成器

    展示时间序列事件
    """

    def __init__(self,
                 title: str,
                 industry: str = 'default',
                 width: int = 1920,
                 height: int = 1080):
        """
        初始化时间线图

        Args:
            title: 图表标题
            industry: 行业类型
            width: 图表宽度
            height: 图表高度
        """
        super().__init__(title, industry, width, height)

    def generate(self, data: Dict) -> str:
        """
        生成时间线图SVG

        Args:
            data: 图表数据
                {
                    'events': [
                        {'year': 年份, 'event': '事件标题', 'description': '详细描述'},
                        ...
                    ]
                }

        Returns:
            svg: SVG字符串
        """
        events = data.get('events', [])

        if not events:
            raise ValueError("时间线图数据不能为空")

        # 开始生成SVG
        svg = self._create_svg_header()
        svg += self._add_background()

        # 添加标题
        svg += self._add_title(self.width // 2, 120, font_size=56)

        # 计算时间线参数
        timeline_left = 200
        timeline_width = self.width - 400
        timeline_y = self.height // 2
        timeline_height = 400

        # 获取时间范围
        years = [event['year'] for event in events]
        min_year = min(years)
        max_year = max(years)
        year_span = max_year - min_year if max_year > min_year else 1

        # 绘制时间轴主线
        primary_color = self.colors.get_primary()
        svg += self._add_line(
            timeline_left, timeline_y,
            timeline_left + timeline_width, timeline_y,
            stroke=primary_color,
            stroke_width=4
        )

        # 绘制年份刻度
        for i in range(max_year - min_year + 1):
            year = min_year + i
            x = timeline_left + (i / year_span) * timeline_width if year_span > 0 else timeline_left

            # 刻度线
            svg += self._add_line(
                int(x), timeline_y - 10,
                int(x), timeline_y + 10,
                stroke='#9ca3af',
                stroke_width=2
            )

            # 年份标签
            svg += self._add_text(
                int(x),
                timeline_y + 40,
                str(year),
                font_size=24,
                color='#6b7280',
                anchor='middle'
            )

        # 绘制事件点和描述（上下交错）
        colors = self.colors.get_categorical(len(events))

        for i, event in enumerate(events):
            year = event['year']
            event_title = event['event']
            description = event.get('description', '')

            # 计算X位置
            x = timeline_left + ((year - min_year) / year_span) * timeline_width if year_span > 0 else timeline_left

            # 上下交错
            is_above = i % 2 == 0
            offset_y = -timeline_height // 2 if is_above else timeline_height // 2

            # 连接线
            svg += self._add_line(
                int(x), timeline_y,
                int(x), timeline_y + offset_y,
                stroke=colors[i % len(colors)],
                stroke_width=3,
                dash_array='5,5'
            )

            # 事件点（大圆）
            svg += self._add_circle(
                int(x), timeline_y,
                r=15,
                fill=colors[i % len(colors)],
                stroke='#ffffff',
                stroke_width=4
            )

            # 事件卡片位置
            card_y = timeline_y + offset_y

            # 事件标题
            title_y = card_y - 10 if is_above else card_y + 10
            svg += self._add_text(
                int(x),
                int(title_y),
                event_title,
                font_size=28,
                color='#1f2937',
                anchor='middle',
                weight='bold'
            )

            # 事件描述
            if description:
                desc_y = title_y - 35 if is_above else title_y + 35
                svg += self._add_text(
                    int(x),
                    int(desc_y),
                    description,
                    font_size=22,
                    color='#6b7280',
                    anchor='middle'
                )

            # 年份标签（在事件点旁）
            year_badge_y = card_y - 70 if is_above else card_y + 70
            svg += self._add_rect(
                int(x) - 40, int(year_badge_y) - 20,
                80, 35,
                fill=colors[i % len(colors)],
                stroke='#ffffff',
                stroke_width=2
            )
            svg += self._add_text(
                int(x),
                int(year_badge_y),
                str(year),
                font_size=24,
                color='#ffffff',
                anchor='middle',
                weight='bold'
            )

        # 添加箭头（时间线右端）
        arrow_x = timeline_left + timeline_width
        arrow_points = [
            (arrow_x, timeline_y),
            (arrow_x + 30, timeline_y - 15),
            (arrow_x + 30, timeline_y + 15)
        ]
        svg += self._add_polygon(
            arrow_points,
            fill=primary_color
        )

        svg += self._create_svg_footer()
        return svg


def main():
    """测试时间线图生成器"""
    print("="*60)
    print("Test: Timeline Chart Generator")
    print("="*60)

    # 测试数据：长护险政策演进
    test_data = {
        'events': [
            {
                'year': 2015,
                'event': '长护险试点启动',
                'description': '15个城市开始试点'
            },
            {
                'year': 2018,
                'event': '扩大试点范围',
                'description': '扩展至49个城市'
            },
            {
                'year': 2020,
                'event': '全国推广',
                'description': '政策全面落地'
            },
            {
                'year': 2022,
                'event': '深化改革',
                'description': '优化支付标准'
            },
            {
                'year': 2024,
                'event': '覆盖1.8亿人',
                'description': '参保人数突破1.8亿'
            }
        ]
    }

    # 生成图表
    chart = TimelineChart(
        '长期护理保险政策演进时间线',
        industry='medical'
    )

    output_path = Path('./output/test_timeline_chart.svg')
    chart.save(test_data, output_path)

    print(f"\n[OK] Timeline chart generated: {output_path}")
    print(f"Events: {len(test_data['events'])}")
    print(f"Year range: {test_data['events'][0]['year']} - {test_data['events'][-1]['year']}")


if __name__ == '__main__':
    main()
