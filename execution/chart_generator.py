"""
图表生成器集成模块

将5种图表类型集成到主控层，提供统一的图表生成接口

功能:
1. 根据行业和数据自动选择合适的图表类型
2. 批量生成图表
3. 快速模式（3-5张核心图表）
4. 全量模式（10+张完整图表）
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from execution.charts import (
    PyramidChart,
    WaterfallChart,
    ComparisonPieChart,
    TimelineChart,
    ScatterMatrixChart
)


class ChartGenerator:
    """
    图表生成器集成

    协调所有图表类型的生成
    """

    def __init__(self, industry: str = 'default', output_dir: Path = None):
        """
        初始化图表生成器

        Args:
            industry: 行业类型（用于配色）
            output_dir: 输出目录
        """
        self.industry = industry
        self.output_dir = output_dir or Path('./output/charts')
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.generated_charts = []

    def generate_core_charts(self, analysis_data: Dict) -> List[Path]:
        """
        生成核心图表（快速模式）

        根据数据自动选择3-5张最重要的图表

        Args:
            analysis_data: 分析结果数据
                {
                    'industry_structure': {...},  # 金字塔图数据
                    'unit_economics': {...},      # 瀑布图数据
                    'payment_structure': {...},    # 对比饼图数据
                    'policy_timeline': {...},      # 时间线图数据
                    'competitive_landscape': {...} # 散点矩阵图数据
                }

        Returns:
            chart_paths: 生成的图表路径列表
        """
        print("\n[Chart Generator] Generating core charts (quick mode)...")

        chart_paths = []

        # 1. 金字塔图（行业结构）- 优先级最高
        if 'industry_structure' in analysis_data:
            try:
                pyramid_data = analysis_data['industry_structure']
                chart = PyramidChart(
                    pyramid_data.get('title', '行业结构金字塔'),
                    industry=self.industry
                )
                output_path = self.output_dir / 'pyramid_industry_structure.svg'
                chart.save(pyramid_data, output_path)
                chart_paths.append(output_path)
                print(f"  [OK] Pyramid chart: {output_path.name}")
            except Exception as e:
                print(f"  [SKIP] Pyramid chart failed: {e}")

        # 2. 瀑布图（单位经济模型）
        if 'unit_economics' in analysis_data:
            try:
                waterfall_data = analysis_data['unit_economics']
                chart = WaterfallChart(
                    waterfall_data.get('title', '单位经济模型'),
                    industry=self.industry
                )
                output_path = self.output_dir / 'waterfall_unit_economics.svg'
                chart.save(waterfall_data, output_path)
                chart_paths.append(output_path)
                print(f"  [OK] Waterfall chart: {output_path.name}")
            except Exception as e:
                print(f"  [SKIP] Waterfall chart failed: {e}")

        # 3. 对比饼图（支付结构）
        if 'payment_structure' in analysis_data:
            try:
                pie_data = analysis_data['payment_structure']
                chart = ComparisonPieChart(
                    pie_data.get('title', '支付结构对比'),
                    industry=self.industry
                )
                output_path = self.output_dir / 'comparison_pie_payment.svg'
                chart.save(pie_data, output_path)
                chart_paths.append(output_path)
                print(f"  [OK] Comparison pie chart: {output_path.name}")
            except Exception as e:
                print(f"  [SKIP] Comparison pie chart failed: {e}")

        # 4. 时间线图（政策演进）
        if 'policy_timeline' in analysis_data:
            try:
                timeline_data = analysis_data['policy_timeline']
                chart = TimelineChart(
                    timeline_data.get('title', '政策演进时间线'),
                    industry=self.industry
                )
                output_path = self.output_dir / 'timeline_policy.svg'
                chart.save(timeline_data, output_path)
                chart_paths.append(output_path)
                print(f"  [OK] Timeline chart: {output_path.name}")
            except Exception as e:
                print(f"  [SKIP] Timeline chart failed: {e}")

        # 5. 散点矩阵图（竞争格局）
        if 'competitive_landscape' in analysis_data:
            try:
                scatter_data = analysis_data['competitive_landscape']
                chart = ScatterMatrixChart(
                    scatter_data.get('title', '竞争格局分析'),
                    industry=self.industry
                )
                output_path = self.output_dir / 'scatter_matrix_competition.svg'
                chart.save(scatter_data, output_path)
                chart_paths.append(output_path)
                print(f"  [OK] Scatter matrix chart: {output_path.name}")
            except Exception as e:
                print(f"  [SKIP] Scatter matrix chart failed: {e}")

        self.generated_charts = chart_paths
        print(f"\n[Chart Generator] Generated {len(chart_paths)} charts")

        return chart_paths

    def generate_all_charts(self, analysis_data: Dict) -> List[Path]:
        """
        生成全量图表（全量模式）

        生成所有可能的图表类型（10+张）

        Args:
            analysis_data: 完整分析结果数据

        Returns:
            chart_paths: 生成的图表路径列表
        """
        print("\n[Chart Generator] Generating all charts (full mode)...")

        # 先生成核心图表
        chart_paths = self.generate_core_charts(analysis_data)

        # 添加趋势图（市场规模趋势）
        if 'market_trend' in analysis_data:
            try:
                from execution.charts.line_chart import LineChart
                trend_data = analysis_data['market_trend']
                chart = LineChart(
                    trend_data.get('title', '市场规模趋势'),
                    industry=self.industry
                )
                output_path = self.output_dir / 'line_market_trend.svg'
                chart.save(trend_data, output_path)
                chart_paths.append(output_path)
                print(f"  [OK] Line chart: {output_path.name}")
            except Exception as e:
                print(f"  [SKIP] Line chart failed: {e}")

        # 添加雷达图（PEST分析）
        if 'pest_radar' in analysis_data:
            try:
                from execution.charts.radar_chart import RadarChart
                radar_data = analysis_data['pest_radar']
                chart = RadarChart(
                    radar_data.get('title', 'PEST分析雷达图'),
                    industry=self.industry
                )
                output_path = self.output_dir / 'radar_pest_analysis.svg'
                chart.save(radar_data, output_path)
                chart_paths.append(output_path)
                print(f"  [OK] Radar chart: {output_path.name}")
            except Exception as e:
                print(f"  [SKIP] Radar chart failed: {e}")

        self.generated_charts = chart_paths
        print(f"\n[Chart Generator] Total generated {len(chart_paths)} charts")

        return chart_paths

    def auto_select_charts(self, data_availability: Dict) -> List[str]:
        """
        根据数据可用性自动选择图表类型

        Args:
            data_availability: 数据可用性字典
                {
                    'industry_structure': True/False,
                    'unit_economics': True/False,
                    ...
                }

        Returns:
            chart_types: 应生成的图表类型列表
        """
        selected_charts = []

        if data_availability.get('industry_structure'):
            selected_charts.append('pyramid')

        if data_availability.get('unit_economics'):
            selected_charts.append('waterfall')

        if data_availability.get('payment_structure'):
            selected_charts.append('comparison_pie')

        if data_availability.get('policy_timeline'):
            selected_charts.append('timeline')

        if data_availability.get('competitive_landscape'):
            selected_charts.append('scatter_matrix')

        return selected_charts

    def get_chart_summary(self) -> Dict:
        """
        获取已生成图表的摘要

        Returns:
            summary: 图表摘要信息
        """
        if not self.generated_charts:
            return {
                'count': 0,
                'charts': [],
                'total_size': 0
            }

        total_size = sum(p.stat().st_size for p in self.generated_charts)

        return {
            'count': len(self.generated_charts),
            'charts': [
                {
                    'name': p.name,
                    'path': str(p),
                    'size': p.stat().st_size
                }
                for p in self.generated_charts
            ],
            'total_size': total_size
        }


def main():
    """测试图表生成器集成"""
    print("="*60)
    print("Test: Chart Generator Integration")
    print("="*60)

    # 模拟分析数据
    mock_analysis_data = {
        'industry_structure': {
            'title': '医疗陪护行业金字塔结构',
            'layers': [
                {'label': '高端市场', 'value': 630, 'unit': '亿元'},
                {'label': '中端市场', 'value': 470, 'unit': '亿元'},
                {'label': '基础市场', 'value': 210, 'unit': '亿元'}
            ]
        },
        'unit_economics': {
            'title': '单位经济模型',
            'items': [
                {'label': '单位收入', 'value': 500, 'type': 'start'},
                {'label': '人力成本', 'value': -200, 'type': 'decrease'},
                {'label': '材料成本', 'value': -100, 'type': 'decrease'},
                {'label': '运营成本', 'value': -50, 'type': 'decrease'},
                {'label': '单位毛利', 'value': 150, 'type': 'end'}
            ],
            'unit': '元'
        },
        'payment_structure': {
            'title': '支付结构演进',
            'left': {
                'title': '当前（2024）',
                'data': {'自费': 70, '保险': 20, '政府': 10}
            },
            'right': {
                'title': '目标（2030）',
                'data': {'自费': 40, '保险': 40, '长护险': 10, '政府': 10}
            }
        }
    }

    # 测试快速模式
    generator = ChartGenerator(industry='medical')

    print("\n--- Quick Mode Test ---")
    quick_charts = generator.generate_core_charts(mock_analysis_data)

    print("\n--- Chart Summary ---")
    summary = generator.get_chart_summary()
    print(f"Generated charts: {summary['count']}")
    print(f"Total size: {summary['total_size'] / 1024:.1f} KB")

    for chart in summary['charts']:
        print(f"  - {chart['name']} ({chart['size'] / 1024:.1f} KB)")


if __name__ == '__main__':
    main()
