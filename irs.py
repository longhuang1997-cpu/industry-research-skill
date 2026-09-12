"""
Industry Research Skill - 统一入口

架构重构（2026-09-12）：
- 精简模块，用Prompt工程替代复杂脚本
- core/research_engine.py: 统一研究引擎
- core/orchestrator.py: 精简主控层
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent
sys.path.insert(0, str(SKILL_ROOT))


def run_research(industry, user_params=None):
    """
    运行行业研究（可被外部调用）

    Args:
        industry: 行业名称
        user_params: 用户参数字典（可选）
            - dimensions: List[str] - 分析维度列表
            - intent: str - 自然语言意图
            - depth: str - 研究深度
            - mode: str - 研究模式（quick/full）

    Returns:
        result: 研究结果字典
    """
    from core.orchestrator import Orchestrator

    # 默认参数
    if user_params is None:
        user_params = {}

    # 设置默认值
    mode = user_params.get('mode', 'quick')

    # 创建orchestrator
    orchestrator = Orchestrator(mode=mode)

    # 执行研究
    result = orchestrator.run(
        industry=industry,
        user_params=user_params
    )

    return result


def main():
    """主函数 - CLI入口"""
    if len(sys.argv) < 2:
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  Industry Research Skill - AI驱动的行业研究工具            ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        print("使用方法:")
        print()
        print("1. 快速研究:")
        print("   python irs.py <行业名称>")
        print("   示例: python irs.py 医疗陪护")
        print()
        print("2. 自然语言:")
        print("   python irs.py <行业名称> --intent \"重点看政策和竞争，快速版\"")
        print()
        print("3. 指定维度:")
        print("   python irs.py <行业名称> --dimensions 政策环境,市场规模,商业模式")
        print()
        print("4. 全量模式:")
        print("   python irs.py <行业名称> --mode full")
        print()
        print("可用维度:")
        print("  政策环境, 市场规模, 商业模式, 竞争格局, 进入壁垒, 风险分析")
        print()
        sys.exit(1)

    industry = sys.argv[1]

    # 解析命令行参数
    mode = 'quick'
    dimensions = None
    intent = None

    # 解析 --mode
    if '--mode' in sys.argv:
        idx = sys.argv.index('--mode')
        if idx + 1 < len(sys.argv):
            mode = sys.argv[idx + 1]

    # 解析 --dimensions
    if '--dimensions' in sys.argv:
        idx = sys.argv.index('--dimensions')
        if idx + 1 < len(sys.argv):
            dimensions = sys.argv[idx + 1].split(',')

    # 解析 --intent
    if '--intent' in sys.argv:
        idx = sys.argv.index('--intent')
        if idx + 1 < len(sys.argv):
            intent = sys.argv[idx + 1]

    # 构建用户参数
    user_params = {'mode': mode}

    if dimensions:
        user_params['dimensions'] = dimensions
    if intent:
        user_params['intent'] = intent

    # 调用研究函数
    result = run_research(industry, user_params)

    # 输出结果
    print("\n" + "="*60)
    if result['status'] == 'success':
        print("[SUCCESS] 研究完成!")
        print("="*60)
        print(f"\n行业: {result['industry']}")
        print(f"模式: {result.get('mode', 'quick')}")
        print(f"报告路径: {result.get('path', '未生成')}")
        print(f"平均质量分: {result.get('quality', {}).get('avg_quality', 0):.2f}")
        print(f"预计时间: {result.get('total_time', 0)} 分钟")
    else:
        print("[ERROR] 研究失败")
        print("="*60)
        print(f"\n错误: {result.get('error', '未知错误')}")


if __name__ == '__main__':
    main()
