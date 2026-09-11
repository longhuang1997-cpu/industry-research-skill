"""
金字塔图生成器

用于展示行业结构层级:
- 顶层: 高端市场/核心资源
- 中层: 主流市场/服务提供者
- 底层: 基础市场/支撑要素

数据格式示例:
{
    'layers': [
        {'label': '顶层市场', 'value': 630, 'unit': '亿元'},
        {'label': '中层市场', 'value': 470, 'unit': '亿元'},
        {'label': '底层市场', 'value': 210, 'unit': '亿元'}
    ],
    'title': '医疗陪护行业金字塔结构'
}
"""

import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from execution.charts.chart_base import ChartBase


class PyramidChart(ChartBase):
    """
    金字塔图生成器

    展示行业层级结构
    """

    def __init__(self,
                 title: str,
                 industry: str = 'default',
                 width: int = 1920,
                 height: int = 1080):
        """
        初始化金字塔图

        Args:
            title: 图表标题
            industry: 行业类型
            width: 图表宽度
            height: 图表高度
        """
        super().__init__(title, industry, width, height)

    def generate(self, data: Dict) -> str:
        """
        生成金字塔图SVG

        Args:
            data: 图表数据
                {
                    'layers': [
                        {'label': '层级名称', 'value': 数值, 'unit': '单位'},
                        ...
                    ]
                }

        Returns:
            svg: SVG字符串
        """
        layers = data.get('layers', [])

        if not layers:
            raise ValueError("金字塔图数据不能为空")

        # 开始生成SVG
        svg = self._create_svg_header()
        svg += self._add_background()

        # 添加标题
        svg += self._add_title(self.width // 2, 120, font_size=56)

        # 计算金字塔参数
        pyramid_top_y = 250
        pyramid_height = 700
        pyramid_max_width = 1200
        pyramid_center_x = self.width // 2

        # 获取渐变色
        colors = self.colors.get_gradient(len(layers))

        # 计算总值（用于确定每层宽度）
        total_value = sum(layer['value'] for layer in layers)

        # 绘制每一层
        current_y = pyramid_top_y
        layer_height = pyramid_height / len(layers)

        for i, layer in enumerate(layers):
            # 计算当前层的宽度（基于金字塔形状）
            # 顶层最窄，底层最宽
            width_ratio = (i + 1) / len(layers)
            layer_width = pyramid_max_width * width_ratio

            # 计算梯形的四个顶点
            if i == 0:
                # 第一层（顶层）- 从顶点开始
                top_width = pyramid_max_width * 0.3  # 顶层宽度固定为30%
                points = [
                    (pyramid_center_x, current_y),  # 顶点
                    (pyramid_center_x, current_y),
                    (pyramid_center_x + layer_width // 2, current_y + layer_height),
                    (pyramid_center_x - layer_width // 2, current_y + layer_height)
                ]
            else:
                # 其他层 - 梯形
                prev_width_ratio = i / len(layers)
                prev_layer_width = pyramid_max_width * prev_width_ratio

                points = [
                    (pyramid_center_x - prev_layer_width // 2, current_y),
                    (pyramid_center_x + prev_layer_width // 2, current_y),
                    (pyramid_center_x + layer_width // 2, current_y + layer_height),
                    (pyramid_center_x - layer_width // 2, current_y + layer_height)
                ]

            # 绘制梯形
            svg += self._add_polygon(
                points,
                fill=colors[i],
                stroke='#ffffff',
                stroke_width=4
            )

            # 添加层级标签
            label_y = current_y + layer_height // 2 + 10
            svg += self._add_text(
                pyramid_center_x,
                label_y,
                layer['label'],
                font_size=36,
                color='#ffffff',
                anchor='middle',
                weight='bold'
            )

            # 添加数值标签
            value_text = f"{layer['value']}{layer.get('unit', '')}"
            svg += self._add_text(
                pyramid_center_x,
                label_y + 45,
                value_text,
                font_size=32,
                color='#ffffff',
                anchor='middle'
            )

            # 添加百分比（如果有总值）
            if total_value > 0:
                percentage = (layer['value'] / total_value) * 100
                percentage_text = f"({percentage:.1f}%)"
                svg += self._add_text(
                    pyramid_center_x,
                    label_y + 85,
                    percentage_text,
                    font_size=28,
                    color='#f0f0f0',
                    anchor='middle'
                )

            # 添加右侧注释（可选）
            annotation = layer.get('annotation', '')
            if annotation:
                annotation_x = pyramid_center_x + layer_width // 2 + 80
                svg += self._add_text(
                    annotation_x,
                    label_y,
                    annotation,
                    font_size=24,
                    color='#6b7280',
                    anchor='start'
                )

            current_y += layer_height

        # 添加底部说明
        svg += self._add_text(
            self.width // 2,
            self.height - 50,
            f"总规模: {total_value}{layers[0].get('unit', '')}",
            font_size=32,
            color='#374151',
            anchor='middle',
            weight='bold'
        )

        svg += self._create_svg_footer()
        return svg


def main():
    """测试金字塔图生成器"""
    print("="*60)
    print("Test: Pyramid Chart Generator")
    print("="*60)

    # 测试数据：医疗陪护行业金字塔
    test_data = {
        'layers': [
            {
                'label': '高端护理市场',
                'value': 630,
                'unit': '亿元',
                'annotation': '专业护理员+高端医疗机构'
            },
            {
                'label': '中端护理市场',
                'value': 470,
                'unit': '亿元',
                'annotation': '普通护理员+一般医疗机构'
            },
            {
                'label': '基础护理市场',
                'value': 210,
                'unit': '亿元',
                'annotation': '家政护理+社区服务'
            }
        ]
    }

    # 生成图表
    chart = PyramidChart(
        '医疗陪护行业金字塔结构（2024年）',
        industry='medical'
    )

    output_path = Path('./output/test_pyramid_chart.svg')
    chart.save(test_data, output_path)

    print(f"\n[OK] Pyramid chart generated: {output_path}")
    print(f"Layers: {len(test_data['layers'])}")
    print(f"Total value: {sum(l['value'] for l in test_data['layers'])} billion")


if __name__ == '__main__':
    main()
