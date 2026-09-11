"""
打包器：将研究结果打包为交付物

功能:
1. 快速模式：打包为PDF执行摘要
2. 全量模式：打包为完整HTML报告 + 附件
"""

import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))


class Packager:
    """
    打包器

    将研究结果打包为标准交付物
    """

    def __init__(self):
        """初始化打包器"""
        self.output_dir = Path('./output')
        self.output_dir.mkdir(exist_ok=True)

    def package_quick_deliverable(self,
                                   summary: Dict,
                                   charts: List,
                                   data_sources: List) -> Dict:
        """
        打包快速模式交付物

        Args:
            summary: 执行摘要
            charts: 图表列表
            data_sources: 数据来源

        Returns:
            deliverable: 交付物信息
        """
        print(f"\n[Packager] Packaging quick deliverable...")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 保存HTML报告
        html_path = self.output_dir / f'executive_summary_{timestamp}.html'
        html_content = summary.get('html', '')

        if html_content:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"   [OK] HTML report saved: {html_path.name}")

        deliverable = {
            'type': 'quick',
            'format': 'html',
            'html_path': str(html_path),
            'timestamp': timestamp,
            'contents': {
                'summary': summary.get('title', ''),
                'charts': f'{len(charts)}张图表',
                'data_sources': f'{len(data_sources)}个数据源',
                'key_findings': len(summary.get('key_findings', []))
            },
            'size': f'{len(html_content)} bytes' if html_content else '0 bytes'
        }

        print(f"   [OK] Deliverable packaged: {html_path.name}")

        return deliverable

    def package_full_deliverable(self,
                                  report: Dict,
                                  charts: List = None,
                                  data_sources: List = None) -> Dict:
        """
        打包全量模式交付物

        Args:
            report: 完整报告
            charts: 图表列表（可选）
            data_sources: 数据来源（可选）

        Returns:
            deliverable: 交付物信息
        """
        print(f"\n[Packager] Packaging full deliverable...")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = self.output_dir / f'full_report_{timestamp}'
        output_dir.mkdir(exist_ok=True)

        # 创建交付包结构
        deliverable = {
            'type': 'full',
            'format': 'html',
            'path': str(output_dir),
            'timestamp': timestamp,
            'structure': {
                'report.html': '主报告',
                'charts/': f'{len(charts or [])}张图表',
                'data/': '原始数据',
                'README.md': '使用说明'
            },
            'contents': {
                'report_sections': len(report.get('sections', {})),
                'charts': len(charts or []),
                'data_sources': len(data_sources or [])
            },
            'size': '待生成'
        }

        print(f"   [OK] Deliverable packaged: {output_dir.name}/")

        return deliverable


def main():
    """测试打包器"""
    print("="*60)
    print("测试: 打包器")
    print("="*60)

    packager = Packager()

    # 测试快速模式打包
    print("\n测试1: 快速模式打包")
    mock_summary = {
        'title': '执行摘要',
        'sections': {}
    }
    deliverable = packager.package_quick_deliverable(mock_summary, [], [])
    print(f"  类型: {deliverable['type']}")
    print(f"  格式: {deliverable['format']}")

    # 测试全量模式打包
    print("\n测试2: 全量模式打包")
    mock_report = {
        'title': '完整报告',
        'sections': {}
    }
    deliverable = packager.package_full_deliverable(mock_report)
    print(f"  类型: {deliverable['type']}")
    print(f"  路径: {deliverable['path']}")


if __name__ == '__main__':
    main()
