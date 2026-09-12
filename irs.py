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
        print("1. 标准研究（30分钟）:")
        print("   python irs.py <行业名称>")
        print("   示例: python irs.py 医疗陪护")
        print()
        print("2. 自定义维度:")
        print("   python irs.py <行业名称> --dimensions 政策环境,市场规模")
        print("   示例: python irs.py 医疗陪护 --dimensions 政策环境,竞争格局")
        print()
        print("3. 自定义深度:")
        print("   python irs.py <行业名称> --depth 10分钟")
        print("   示例: python irs.py 医疗陪护 --depth 快速")
        print()
        print("4. 组合使用:")
        print("   python irs.py 医疗陪护 --dimensions 政策环境 --depth 10分钟")
        print()
        print("可用维度: 政策环境, 市场规模, 商业模式, 竞争格局, 进入壁垒, 产业链, 风险分析, 机会识别")
        print("可用深度: 快速(10分钟), 标准(30分钟), 深度(60分钟)")
        print()
        sys.exit(1)

    industry = sys.argv[1]

    # 解析命令行参数
    mode = 'quick'
    dimensions = None
    depth = None

    # 解析 --mode
    if '--mode' in sys.argv:
        idx = sys.argv.index('--mode')
        if idx + 1 < len(sys.argv):
            mode = sys.argv[idx + 1]

    # 解析 --dimensions (例如: --dimensions 政策环境,市场规模)
    if '--dimensions' in sys.argv:
        idx = sys.argv.index('--dimensions')
        if idx + 1 < len(sys.argv):
            dimensions = sys.argv[idx + 1].split(',')

    # 解析 --depth (例如: --depth 10分钟)
    if '--depth' in sys.argv:
        idx = sys.argv.index('--depth')
        if idx + 1 < len(sys.argv):
            depth = sys.argv[idx + 1]

    # 兼容旧的 --interactive
    if '--interactive' in sys.argv:
        mode = 'full'

    # 调用orchestrator作为主控
    from orchestrator.orchestrator import IndustryResearchOrchestrator

    orchestrator = IndustryResearchOrchestrator(mode=mode)

    # 构建用户参数
    user_params = {
        'industry': industry,
        'web_search': True,
        'mode': mode
    }

    if dimensions:
        user_params['dimensions'] = dimensions

    if depth:
        user_params['depth'] = depth

    result = orchestrator.run(
        industry_name=industry,
        user_params=user_params
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
