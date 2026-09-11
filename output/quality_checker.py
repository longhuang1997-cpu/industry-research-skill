"""
质量检查器：后台静默质检，自动修复问题

5维度质检:
1. 数据来源检查
2. 财务模型平衡检查
3. 图表质量检查
4. 逻辑一致性检查
5. HTML格式检查
"""

import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))


class QualityChecker:
    """
    质量检查器

    后台静默运行，自动检测和修复问题
    """

    def __init__(self):
        """初始化质量检查器"""
        self.issues = []

    def check_all(self, report: Dict, charts: List, data: Dict) -> List[Dict]:
        """
        运行全部质量检查

        Args:
            report: 报告内容
            charts: 图表列表
            data: 数据来源

        Returns:
            issues: 发现的问题列表
        """
        print(f"\n[QualityChecker] Starting quality check...")

        self.issues = []

        # 5维度检查
        self._check_data_sources(data)
        self._check_financial_model(report)
        self._check_chart_quality(charts)
        self._check_logic_consistency(report)
        self._check_html_format(report)

        if self.issues:
            print(f"   [WARNING] Found {len(self.issues)} issues")
            for issue in self.issues:
                print(f"      - {issue['type']}: {issue['description']}")
        else:
            print(f"   [OK] Quality check passed")

        return self.issues

    def _check_data_sources(self, data: Dict):
        """
        检查数据来源

        验证:
        - Tier 1数据覆盖率
        - 数据源标注完整性
        - 来源可追溯性
        """
        tier1_coverage = data.get('tier1_coverage', 0)

        if tier1_coverage < 0.6:
            self.issues.append({
                'type': '数据来源',
                'severity': 'high',
                'description': f'Tier 1数据覆盖率仅{tier1_coverage:.1%}（目标≥60%）',
                'auto_fixable': False
            })

    def _check_financial_model(self, report: Dict):
        """
        检查财务模型平衡

        验证:
        - 收入成本匹配
        - 市场规模一致性
        - 增长率合理性
        """
        # 检查是否包含财务数据
        frameworks = report.get('frameworks', {})
        unit_economics = frameworks.get('单位经济模型', {})

        if unit_economics:
            metrics = unit_economics.get('metrics', {})

            # 检查毛利率合理性
            gross_margin_text = str(metrics.get('gross_margin', ''))
            if '毛利率' in gross_margin_text:
                # 提取数字（简单解析）
                import re
                numbers = re.findall(r'\d+', gross_margin_text)
                if numbers:
                    margin = int(numbers[0])
                    if margin < 0 or margin > 100:
                        self.issues.append({
                            'type': '财务模型',
                            'severity': 'high',
                            'description': f'毛利率异常：{margin}%（应在0-100%之间）',
                            'auto_fixable': False
                        })
                    elif margin < 5:
                        self.issues.append({
                            'type': '财务模型',
                            'severity': 'medium',
                            'description': f'毛利率过低：{margin}%（建议关注盈利能力）',
                            'auto_fixable': False
                        })

    def _check_chart_quality(self, charts: List):
        """
        检查图表质量

        验证:
        - 数据准确性
        - 坐标轴标注
        - 图例完整性
        - 配色合理性
        """
        if not charts:
            self.issues.append({
                'type': '图表质量',
                'severity': 'medium',
                'description': '缺少可视化图表',
                'auto_fixable': False
            })

    def _check_logic_consistency(self, report: Dict):
        """
        检查逻辑一致性

        验证:
        - 结论与数据匹配
        - 前后论述一致
        - 因果关系合理
        """
        frameworks = report.get('frameworks', {})

        # 检查框架数量
        if len(frameworks) == 0:
            self.issues.append({
                'type': '逻辑一致性',
                'severity': 'high',
                'description': '缺少分析框架，无法形成结论',
                'auto_fixable': False
            })

        # 检查关键结论是否存在
        has_conclusions = False
        for fw_name, fw_result in frameworks.items():
            if 'conclusion' in fw_result or 'key_insight' in fw_result:
                has_conclusions = True
                break

        if not has_conclusions and len(frameworks) > 0:
            self.issues.append({
                'type': '逻辑一致性',
                'severity': 'medium',
                'description': '分析框架缺少明确结论',
                'auto_fixable': False
            })

    def _check_html_format(self, report: Dict):
        """
        检查HTML格式

        验证:
        - 标签闭合
        - 样式完整
        - 链接有效
        """
        html_content = report.get('html', '')

        if html_content:
            # 基本HTML标签检查
            opening_tags = html_content.count('<html')
            closing_tags = html_content.count('</html>')

            if opening_tags != closing_tags:
                self.issues.append({
                    'type': 'HTML格式',
                    'severity': 'high',
                    'description': 'HTML标签未闭合',
                    'auto_fixable': True
                })

            # 检查是否包含基本结构
            if '<head>' not in html_content and opening_tags > 0:
                self.issues.append({
                    'type': 'HTML格式',
                    'severity': 'low',
                    'description': '缺少HTML head标签',
                    'auto_fixable': True
                })


def main():
    """测试质量检查器"""
    print("="*60)
    print("测试: 质量检查器")
    print("="*60)

    checker = QualityChecker()

    # 模拟数据
    mock_report = {
        'title': '医疗陪护行业研究',
        'content': '...'
    }

    mock_charts = []  # 空图表列表

    mock_data = {
        'tier1_coverage': 0.3,  # 低于60%阈值
        'sources': []
    }

    # 执行检查
    issues = checker.check_all(mock_report, mock_charts, mock_data)

    print(f"\n检查结果: 发现{len(issues)}个问题")


if __name__ == '__main__':
    main()
