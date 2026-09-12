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
    print("✅ 研究完成！")
    print("="*60)
    print(f"\n状态: {result['status']}")
    print(f"模式: {'快速模式 (70分钟)' if result['mode'] == 'quick' else '全量模式 (3-5小时)'}")
    print(f"行业: {result['industry']}")

    if result['status'] == 'success':
        print("\n📊 交付物统计:")
        if 'path' in result:
            print(f"  • 专业报告: {result['path']}")
        if 'charts' in result:
            print(f"  • 图表数量: {result['charts']}张")
        if 'data_sources' in result:
            print(f"  • 数据源: {result['data_sources']}个")
        if 'tier1_coverage' in result:
            print(f"  • 数据质量: Tier 1覆盖率 {result['tier1_coverage']:.1%}")
        if 'ai_quality_avg' in result:
            print(f"  • AI分析质量: {result['ai_quality_avg']:.2f}/1.00")
        if 'quality_issues' in result:
            if result['quality_issues'] == 0:
                print(f"  • 质量检查: ✓ 通过")
            else:
                print(f"  • 质量检查: ⚠️  {result['quality_issues']}个问题（可接受）")

    if 'note' in result:
        print(f"\n📝 备注: {result['note']}")


if __name__ == '__main__':
    main()
