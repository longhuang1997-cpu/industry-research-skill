"""
Industry Research Skill - 统一入口
调用orchestrator.py作为主控层
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent
sys.path.insert(0, str(SKILL_ROOT))


def main():
    """主函数 - 使用orchestrator作为主控"""
    if len(sys.argv) < 2:
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  Industry Research Skill - AI驱动的行业研究工具            ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        print("使用方法:")
        print()
        print("1. 快速模式（70分钟）:")
        print("   python irs.py <行业名称>")
        print("   示例: python irs.py 医疗陪护")
        print()
        print("2. 全量模式（3-5小时）:")
        print("   python irs.py <行业名称> --mode full")
        print("   示例: python irs.py 医疗陪护 --mode full")
        print()
        sys.exit(1)

    industry = sys.argv[1]

    # 判断模式
    mode = 'quick'
    if len(sys.argv) > 2:
        if '--mode' in sys.argv:
            idx = sys.argv.index('--mode')
            if idx + 1 < len(sys.argv):
                mode = sys.argv[idx + 1]
        elif sys.argv[2] == '--interactive':
            # 兼容旧的交互模式，映射到full mode
            mode = 'full'

    # 调用orchestrator作为主控
    from orchestrator.orchestrator import IndustryResearchOrchestrator

    orchestrator = IndustryResearchOrchestrator(mode=mode)

    result = orchestrator.run(
        industry_name=industry,
        user_params={
            'industry': industry,
            'web_search': True,
            'mode': mode
        }
    )

    # 输出结果
    print("\n" + "="*60)
    print("[OK] Research Complete!")
    print("="*60)
    print(f"Status: {result['status']}")
    print(f"Mode: {result['mode']}")
    print(f"Industry: {result['industry']}")
    if 'path' in result:
        print(f"Deliverable: {result['path']}")
    if 'charts' in result:
        print(f"Charts: {result['charts']}")
    if 'data_sources' in result:
        print(f"Data sources: {result['data_sources']}")
    if 'tier1_coverage' in result:
        print(f"Tier 1 coverage: {result['tier1_coverage']:.1%}")
    if 'quality_issues' in result:
        print(f"Quality issues: {result['quality_issues']}")
    if 'ai_quality_avg' in result:
        print(f"AI Analysis Avg Quality: {result['ai_quality_avg']:.2f}")
    if 'note' in result:
        print(f"Note: {result['note']}")


if __name__ == '__main__':
    main()
