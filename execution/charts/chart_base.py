"""
图表基类

所有图表类型的共同基础:
- SVG生成
- 配色方案集成
- 标注和标签
- 保存功能
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from execution.styles import ColorSchemeManager


class ChartBase(ABC):
    """
    图表基类

    所有图表必须继承此类并实现generate()方法
    """

    def __init__(self,
                 title: str,
                 industry: str = 'default',
                 width: int = 1920,
                 height: int = 1080):
        """
        初始化图表

        Args:
            title: 图表标题
            industry: 行业类型（用于配色）
            width: 图表宽度（像素）
            height: 图表高度（像素）
        """
        self.title = title
        self.industry = industry
        self.width = width
        self.height = height

        # 获取配色方案
        color_manager = ColorSchemeManager()
        self.colors = color_manager.get_scheme(industry)

        # SVG元素列表
        self.svg_elements = []

    @abstractmethod
    def generate(self, data: Dict) -> str:
        """
        生成SVG图表

        Args:
            data: 图表数据

        Returns:
            svg: SVG字符串
        """
        pass

    def save(self, data: Dict, output_path: Path) -> Path:
        """
        生成并保存图表

        Args:
            data: 图表数据
            output_path: 输出路径

        Returns:
            saved_path: 保存的文件路径
        """
        svg_content = self.generate(data)

        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 保存SVG文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        file_size = output_path.stat().st_size / 1024  # KB
        print(f"   [OK] Saved: {output_path.name} ({file_size:.1f} KB)")

        return output_path

    def _create_svg_header(self) -> str:
        """创建SVG头部"""
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{self.width}" height="{self.height}"
     xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {self.width} {self.height}">
'''

    def _create_svg_footer(self) -> str:
        """创建SVG尾部"""
        return '</svg>'

    def _add_background(self) -> str:
        """添加背景"""
        bg_color = self.colors.get_background()
        return f'<rect width="{self.width}" height="{self.height}" fill="{bg_color}"/>\n'

    def _add_title(self, x: int, y: int, font_size: int = 48) -> str:
        """
        添加标题

        Args:
            x: X坐标
            y: Y坐标
            font_size: 字体大小
        """
        return f'''<text x="{x}" y="{y}"
         font-size="{font_size}"
         font-weight="bold"
         fill="#1f2937"
         text-anchor="middle">{self.title}</text>\n'''

    def _add_text(self,
                  x: int,
                  y: int,
                  text: str,
                  font_size: int = 24,
                  color: str = '#374151',
                  anchor: str = 'start',
                  weight: str = 'normal') -> str:
        """
        添加文本

        Args:
            x: X坐标
            y: Y坐标
            text: 文本内容
            font_size: 字体大小
            color: 文本颜色
            anchor: 文本锚点 (start/middle/end)
            weight: 字体粗细 (normal/bold)
        """
        return f'''<text x="{x}" y="{y}"
         font-size="{font_size}"
         font-weight="{weight}"
         fill="{color}"
         text-anchor="{anchor}">{text}</text>\n'''

    def _add_rect(self,
                  x: int,
                  y: int,
                  width: int,
                  height: int,
                  fill: str,
                  stroke: Optional[str] = None,
                  stroke_width: int = 2) -> str:
        """
        添加矩形

        Args:
            x: X坐标
            y: Y坐标
            width: 宽度
            height: 高度
            fill: 填充颜色
            stroke: 边框颜色
            stroke_width: 边框宽度
        """
        stroke_attr = f'stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ''
        return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}" {stroke_attr}/>\n'

    def _add_circle(self,
                    cx: int,
                    cy: int,
                    r: int,
                    fill: str,
                    stroke: Optional[str] = None,
                    stroke_width: int = 2) -> str:
        """
        添加圆形

        Args:
            cx: 圆心X坐标
            cy: 圆心Y坐标
            r: 半径
            fill: 填充颜色
            stroke: 边框颜色
            stroke_width: 边框宽度
        """
        stroke_attr = f'stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ''
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {stroke_attr}/>\n'

    def _add_line(self,
                  x1: int,
                  y1: int,
                  x2: int,
                  y2: int,
                  stroke: str = '#9ca3af',
                  stroke_width: int = 2,
                  dash_array: Optional[str] = None) -> str:
        """
        添加直线

        Args:
            x1: 起点X
            y1: 起点Y
            x2: 终点X
            y2: 终点Y
            stroke: 线条颜色
            stroke_width: 线条宽度
            dash_array: 虚线样式 (如 "5,5")
        """
        dash_attr = f'stroke-dasharray="{dash_array}"' if dash_array else ''
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}" {dash_attr}/>\n'

    def _add_polygon(self,
                     points: List[Tuple[int, int]],
                     fill: str,
                     stroke: Optional[str] = None,
                     stroke_width: int = 2) -> str:
        """
        添加多边形

        Args:
            points: 顶点坐标列表 [(x1,y1), (x2,y2), ...]
            fill: 填充颜色
            stroke: 边框颜色
            stroke_width: 边框宽度
        """
        points_str = ' '.join([f'{x},{y}' for x, y in points])
        stroke_attr = f'stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ''
        return f'<polygon points="{points_str}" fill="{fill}" {stroke_attr}/>\n'

    def _add_path(self,
                  d: str,
                  fill: str = 'none',
                  stroke: str = '#000',
                  stroke_width: int = 2) -> str:
        """
        添加路径

        Args:
            d: 路径数据
            fill: 填充颜色
            stroke: 线条颜色
            stroke_width: 线条宽度
        """
        return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>\n'

    def _add_legend(self,
                    items: List[Dict],
                    x: int,
                    y: int,
                    item_width: int = 200) -> str:
        """
        添加图例

        Args:
            items: 图例项列表 [{'label': '标签', 'color': '#xxx'}, ...]
            x: 图例起始X坐标
            y: 图例起始Y坐标
            item_width: 每个图例项的宽度
        """
        legend_html = '<g id="legend">\n'

        for i, item in enumerate(items):
            item_x = x + (i * item_width)

            # 颜色方块
            legend_html += self._add_rect(
                item_x, y - 10, 20, 20,
                fill=item['color']
            )

            # 标签
            legend_html += self._add_text(
                item_x + 30, y + 5,
                item['label'],
                font_size=20,
                color='#374151'
            )

        legend_html += '</g>\n'
        return legend_html


def main():
    """测试图表基类"""
    print("="*60)
    print("测试: 图表基类")
    print("="*60)

    # 创建一个简单的测试图表
    class TestChart(ChartBase):
        def generate(self, data: Dict) -> str:
            svg = self._create_svg_header()
            svg += self._add_background()
            svg += self._add_title(self.width // 2, 100)

            # 添加一个简单的矩形
            svg += self._add_rect(
                self.width // 2 - 100,
                self.height // 2 - 50,
                200, 100,
                fill=self.colors.get_primary()
            )

            # 添加文本
            svg += self._add_text(
                self.width // 2,
                self.height // 2,
                '测试图表',
                font_size=32,
                anchor='middle'
            )

            svg += self._create_svg_footer()
            return svg

    # 测试生成
    chart = TestChart('测试图表基类', industry='medical')
    output_path = Path('./output/test_chart_base.svg')
    output_path.parent.mkdir(exist_ok=True)

    chart.save({}, output_path)
    print(f"\n[OK] Test chart generated: {output_path}")


if __name__ == '__main__':
    main()
