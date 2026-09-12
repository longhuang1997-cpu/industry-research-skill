"""
Industry Research Skill - 统一入口
支持两种模式：
1. 小白钩子模式（一次性命令）：python irs.py "医疗陪护"
2. 交互深度模式：python irs.py "医疗陪护" --interactive
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent
sys.path.insert(0, str(SKILL_ROOT))


def quick_hook_mode(industry: str):
    """
    小白钩子模式：10分钟快速洞察

    目标：展示能力，吸引用户深入使用
    """
    print("\n" + "="*60)
    print(f"🎯 正在为您生成【{industry}】行业快速洞察...")
    print("="*60)

    from execution.consulting_ai_analyzer import ConsultingAIAnalyzer

    analyzer = ConsultingAIAnalyzer()

    # 快速行业画像
    print("\n[1/4] 行业定位...")
    profile = analyzer._analyze_industry_profile(industry)

    # 生成3个核心洞察
    print("[2/4] 政策环境分析...")
    policy = analyzer._analyze_policy_environment(industry, {})

    print("[3/4] 市场规模测算...")
    market = analyzer._analyze_market_size(industry, {})

    print("[4/4] 战略建议生成...")
    strategy = analyzer._generate_strategic_recommendations(
        industry,
        {'policy': policy, 'market_size': market}
    )

    print("\n" + "="*60)
    print("✅ 报告已生成！")
    print("="*60)

    # 展示结果
    print(f"\n📋 【{industry}】行业快速洞察\n")

    print("【行业画像】")
    print(profile['summary'])

    print(f"\n【政策环境】（质量分数: {policy['quality_score']:.2f}）")
    print(policy['content'][:200] + "...\n")

    print(f"【市场规模】（质量分数: {market['quality_score']:.2f}）")
    print(market['content'][:200] + "...\n")

    print("【战略建议】")
    print(strategy['content'][:200] + "...\n")

    # 保存完整报告
    output_file = f"output/{industry}_quick_insight.html"
    print(f"📄 完整报告已保存: {output_file}")
    print("   包含：行业画像、政策环境、市场规模、战略建议\n")

    print("💡 想要更深入的分析？运行：")
    print(f"   python irs.py \"{industry}\" --interactive")
    print("\n")


def interactive_mode(industry: str):
    """
    交互深度模式：30-60分钟多轮深度研究
    """
    from interactive_researcher import InteractiveResearcher

    researcher = InteractiveResearcher()
    researcher.start_research(industry)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  Industry Research Skill - AI驱动的行业研究工具            ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        print("使用方法:")
        print()
        print("1. 快速模式（小白钩子 - 10分钟）:")
        print("   python irs.py <行业名称>")
        print("   示例: python irs.py 医疗陪护")
        print()
        print("2. 交互模式（深度研究 - 30-60分钟）:")
        print("   python irs.py <行业名称> --interactive")
        print("   示例: python irs.py 医疗陪护 --interactive")
        print()
        sys.exit(1)

    industry = sys.argv[1]

    # 判断模式
    if len(sys.argv) > 2 and sys.argv[2] == '--interactive':
        # 交互深度模式
        interactive_mode(industry)
    else:
        # 快速钩子模式
        quick_hook_mode(industry)


if __name__ == '__main__':
    main()
