"""
报告生成器：生成结构化的研究报告

功能:
1. 快速模式：生成1页执行摘要（PDF）
2. 全量模式：生成完整HTML报告
"""

import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))


class ReportGenerator:
    """
    报告生成器

    根据分析结果生成报告
    """

    def __init__(self):
        """初始化报告生成器"""
        pass

    def generate_executive_summary(self,
                                    analysis: Dict,
                                    max_pages: int = 1) -> Dict:
        """
        生成执行摘要（快速模式）

        Args:
            analysis: 分析结果
            max_pages: 最大页数（默认1页A4）

        Returns:
            summary: 执行摘要内容
        """
        print(f"\n[ReportGenerator] Generating executive summary (max {max_pages} page(s))...")

        # 提取关键发现
        frameworks = analysis.get('frameworks', {})
        key_findings = []

        for fw_name, fw_result in frameworks.items():
            conclusion = fw_result.get('conclusion', '')
            if conclusion:
                key_findings.append({
                    'framework': fw_name,
                    'weight': fw_result.get('weight', 0),
                    'conclusion': conclusion
                })

        # 按权重排序
        key_findings.sort(key=lambda x: x.get('weight', 0), reverse=True)

        # 生成HTML内容
        html_content = self._generate_summary_html(key_findings[:5])

        summary = {
            'title': '行业研究执行摘要',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'key_findings': [f['conclusion'] for f in key_findings[:5]],
            'frameworks_applied': len(frameworks),
            'format': 'html',
            'html': html_content,
            'pages': 1
        }

        print(f"   [OK] Executive summary complete")

        return summary

    def _generate_summary_html(self, key_findings: List[Dict]) -> str:
        """生成执行摘要HTML"""
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Executive Summary</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 10px;
        }
        .insight {
            margin: 20px 0;
            padding: 15px 20px;
            background: #f8f9fa;
            border-left: 4px solid #3b82f6;
            border-radius: 4px;
        }
        .framework {
            font-weight: bold;
            color: #3b82f6;
            margin-bottom: 8px;
        }
        .weight {
            color: #6b7280;
            font-size: 0.9em;
        }
        .conclusion {
            margin-top: 5px;
            color: #4b5563;
        }
    </style>
</head>
<body>
    <h1>Executive Summary - Industry Research</h1>
    <p><strong>Date:</strong> """ + datetime.now().strftime('%Y-%m-%d') + """</p>
"""

        if key_findings:
            html += """    <h2>Key Findings</h2>"""
            for i, finding in enumerate(key_findings, 1):
                html += f"""
    <div class="insight">
        <div class="framework">{i}. {finding['framework']} <span class="weight">(Weight: {finding.get('weight', 'N/A')})</span></div>
        <div class="conclusion">{finding.get('conclusion', 'N/A')}</div>
    </div>
"""
        else:
            html += """    <p><em>No key findings available.</em></p>"""

        html += """
</body>
</html>
"""
        return html

    def generate_full_report(self,
                            analysis: Dict,
                            charts: List,
                            insights: List) -> Dict:
        """
        生成完整HTML报告（全量模式）

        Args:
            analysis: 分析结果
            charts: 图表列表
            insights: 洞察列表

        Returns:
            report: 完整报告
        """
        print(f"\n[ReportGenerator] Generating full HTML report...")

        # HTML报告结构
        report = {
            'title': '行业深度研究报告',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'sections': {
                '执行摘要': self._generate_executive_summary_section(),
                '行业定义': self._generate_industry_definition_section(analysis),
                '框架分析': self._generate_framework_analysis_section(analysis),
                '洞察与建议': self._generate_insights_section(insights),
                '可视化': self._generate_visualization_section(charts),
                '数据来源': self._generate_data_sources_section(analysis)
            },
            'format': 'html',
            'file_size': '110KB+'
        }

        print(f"   [OK] Full report complete")

        return report

    def _generate_executive_summary_section(self) -> str:
        """生成执行摘要章节"""
        return """
        <section id="executive-summary">
            <h2>执行摘要</h2>
            <p>核心结论（待实现）</p>
        </section>
        """

    def _generate_industry_definition_section(self, analysis: Dict) -> str:
        """生成行业定义章节"""
        return """
        <section id="industry-definition">
            <h2>行业定义</h2>
            <p>行业定义内容（待实现）</p>
        </section>
        """

    def _generate_framework_analysis_section(self, analysis: Dict) -> str:
        """生成框架分析章节"""
        frameworks_html = ""

        for fw_name, fw_result in analysis.get('frameworks', {}).items():
            frameworks_html += f"""
            <div class="framework-section">
                <h3>{fw_name}</h3>
                <p>权重: {fw_result.get('weight', 'N/A')}</p>
                <p>结论: {fw_result.get('conclusion', '待实现')}</p>
            </div>
            """

        return f"""
        <section id="framework-analysis">
            <h2>框架分析</h2>
            {frameworks_html}
        </section>
        """

    def _generate_insights_section(self, insights: List) -> str:
        """生成洞察与建议章节"""
        return """
        <section id="insights">
            <h2>洞察与建议</h2>
            <p>反常识洞察（待实现）</p>
        </section>
        """

    def _generate_visualization_section(self, charts: List) -> str:
        """生成可视化章节"""
        return """
        <section id="visualization">
            <h2>可视化</h2>
            <p>图表展示（待实现）</p>
        </section>
        """

    def _generate_data_sources_section(self, analysis: Dict) -> str:
        """生成数据来源章节"""
        return """
        <section id="data-sources">
            <h2>数据来源</h2>
            <p>数据来源清单（待实现）</p>
        </section>
        """


def main():
    """测试报告生成器"""
    print("="*60)
    print("测试: 报告生成器")
    print("="*60)

    generator = ReportGenerator()

    # 模拟分析结果
    mock_analysis = {
        'frameworks': {
            'PEST分析': {
                'weight': '30%',
                'conclusion': 'PEST结论'
            }
        }
    }

    # 测试执行摘要
    print("\n测试1: 执行摘要")
    summary = generator.generate_executive_summary(mock_analysis, max_pages=1)
    print(f"  标题: {summary['title']}")
    print(f"  关键发现数: {len(summary['key_findings'])}")
    print(f"  应用框架数: {summary['frameworks_applied']}")

    # 测试完整报告
    print("\n测试2: 完整报告")
    report = generator.generate_full_report(mock_analysis, [], [])
    print(f"  标题: {report['title']}")
    print(f"  章节数: {len(report['sections'])}")


if __name__ == '__main__':
    main()
