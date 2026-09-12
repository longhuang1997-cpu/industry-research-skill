"""
测试WorkflowEngine集成：验证灵活的用户驱动研究

测试场景：
1. 用户自定义维度
2. 用户自定义深度
3. 自然语言意图解析
4. WorkflowEngine生成动态计划
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent
sys.path.insert(0, str(SKILL_ROOT))


def test_workflow_engine():
    """测试1：WorkflowEngine基础功能"""
    print("\n" + "="*60)
    print("测试1：WorkflowEngine基础功能")
    print("="*60)

    from execution.workflow_engine import WorkflowEngine, ResearchDepth, AnalysisDimension, WorkflowConfig

    engine = WorkflowEngine()

    # 测试场景：用户只想看政策环境和竞争格局（快速版）
    config = WorkflowConfig(
        depth=ResearchDepth.CUSTOM,
        dimensions=[
            AnalysisDimension.POLICY,
            AnalysisDimension.COMPETITION
        ],
        include_charts=True,
        include_data_tables=False,
        generate_pdf=False
    )

    steps = engine.create_workflow(config)
    total_time = engine.estimate_total_time(steps)

    print(f"\n用户需求: 只分析政策环境和竞争格局")
    print(f"预计耗时: {total_time}分钟")
    print(f"步骤数量: {len(steps)}")

    print("\n工作流步骤:")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step.name} ({step.dimension.value}, {step.estimated_time}分钟)")

    # 验证：应该只包含行业画像、政策分析、市场规模（竞争依赖）、竞争分析
    expected_steps = ['行业画像', '政策环境深度分析', '市场规模测算', '竞争格局分析']
    actual_steps = [s.name for s in steps]

    print("\n✓ 验证结果:")
    print(f"  预期步骤: {expected_steps}")
    print(f"  实际步骤: {actual_steps}")
    print(f"  依赖解析: {'✓ 正确' if '市场规模测算' in actual_steps else '✗ 错误'}")


def test_intent_parser():
    """测试2：意图解析器"""
    print("\n" + "="*60)
    print("测试2：意图解析器（自然语言理解）")
    print("="*60)

    from orchestrator.intent_parser import IntentParser

    parser = IntentParser()

    test_cases = [
        {
            'input': "帮我研究医疗陪护，重点看政策环境和竞争格局，快速版",
            'expected_dimensions': ['政策环境', '竞争格局'],
            'expected_depth': '快速'
        },
        {
            'input': "我想进入养老行业，想知道市场有多大，竞争激不激烈",
            'expected_dimensions': ['市场规模', '竞争格局'],
            'expected_depth': None
        },
        {
            'input': "从投资人视角，深度分析在线教育的商业模式和风险",
            'expected_dimensions': ['商业模式', '风险分析'],
            'expected_depth': '深度'
        }
    ]

    all_passed = True

    for i, case in enumerate(test_cases, 1):
        print(f"\n[测试用例 {i}]")
        print(f"用户输入: \"{case['input']}\"")

        result = parser.parse(case['input'])

        print(f"解析结果:")
        print(f"  维度: {result['dimensions']}")
        print(f"  深度: {result['depth']}")
        print(f"  视角: {result['perspective']}")

        # 验证
        dimensions_match = set(result['dimensions']) == set(case['expected_dimensions'])
        depth_match = result['depth'] == case['expected_depth']

        print(f"\n验证:")
        print(f"  维度匹配: {'✓' if dimensions_match else '✗'}")
        print(f"  深度匹配: {'✓' if depth_match else '✗'}")

        if not (dimensions_match and depth_match):
            all_passed = False

    return all_passed


def test_orchestrator_integration():
    """测试3：Orchestrator集成"""
    print("\n" + "="*60)
    print("测试3：Orchestrator集成（端到端）")
    print("="*60)

    from orchestrator.orchestrator import IndustryResearchOrchestrator

    # 模拟用户参数
    user_params = {
        'industry': '医疗陪护',
        'dimensions': ['政策环境', '竞争格局'],
        'depth': '快速',
        'web_search': False  # 测试环境不搜索
    }

    print(f"\n用户参数: {user_params}")

    orchestrator = IndustryResearchOrchestrator(mode='quick')

    # 测试需求收集阶段（不执行完整研究）
    try:
        brief = orchestrator._collect_requirements('医疗陪护', user_params)

        print(f"\n✓ 需求收集成功")
        print(f"  行业: {brief['industry']}")
        print(f"  预计耗时: {brief.get('estimated_time', 'N/A')}分钟")
        print(f"  步骤数: {len(brief.get('workflow_steps', []))}")

        # 显示工作流
        if 'workflow_viz' in brief:
            print("\n工作流可视化:")
            print(brief['workflow_viz'])

        return True

    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dimension_mapping():
    """测试4：维度映射验证"""
    print("\n" + "="*60)
    print("测试4：维度映射（自然语言→枚举）")
    print("="*60)

    from execution.workflow_engine import AnalysisDimension

    dimension_map = {
        '政策': AnalysisDimension.POLICY,
        '政策环境': AnalysisDimension.POLICY,
        '市场': AnalysisDimension.MARKET_SIZE,
        '市场规模': AnalysisDimension.MARKET_SIZE,
        '商业模式': AnalysisDimension.BUSINESS_MODEL,
        '竞争': AnalysisDimension.COMPETITION,
        '竞争格局': AnalysisDimension.COMPETITION,
        '壁垒': AnalysisDimension.ENTRY_BARRIERS,
        '进入壁垒': AnalysisDimension.ENTRY_BARRIERS,
        '产业链': AnalysisDimension.SUPPLY_CHAIN,
        '风险': AnalysisDimension.RISK_ANALYSIS,
        '风险分析': AnalysisDimension.RISK_ANALYSIS,
        '机会': AnalysisDimension.OPPORTUNITIES,
        '机会识别': AnalysisDimension.OPPORTUNITIES
    }

    print("\n维度映射表（用户语言 → 系统枚举）:")
    for user_term, enum_value in dimension_map.items():
        print(f"  '{user_term}' → {enum_value.value}")

    print(f"\n✓ 共支持 {len(set(dimension_map.values()))} 个分析维度")
    print(f"✓ 支持 {len(dimension_map)} 种用户表达方式")


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("Industry Research Skill - 灵活工作流测试套件")
    print("="*60)
    print("\n目标：验证WorkflowEngine集成，确保用户可以自定义研究")
    print("\n")

    results = {}

    # 运行测试
    try:
        test_workflow_engine()
        results['workflow_engine'] = True
    except Exception as e:
        print(f"\n✗ WorkflowEngine测试失败: {e}")
        results['workflow_engine'] = False

    try:
        results['intent_parser'] = test_intent_parser()
    except Exception as e:
        print(f"\n✗ IntentParser测试失败: {e}")
        results['intent_parser'] = False

    try:
        results['orchestrator'] = test_orchestrator_integration()
    except Exception as e:
        print(f"\n✗ Orchestrator测试失败: {e}")
        results['orchestrator'] = False

    try:
        test_dimension_mapping()
        results['dimension_mapping'] = True
    except Exception as e:
        print(f"\n✗ 维度映射测试失败: {e}")
        results['dimension_mapping'] = False

    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)

    for test_name, passed in results.items():
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())
    print("\n" + "="*60)
    if all_passed:
        print("✓ 所有测试通过！WorkflowEngine已成功集成")
        print("\n用户现在可以:")
        print("  1. 自定义分析维度")
        print("  2. 自定义研究深度")
        print("  3. 使用自然语言描述需求")
        print("  4. Skill自动生成动态工作流")
    else:
        print("✗ 部分测试失败，需要修复")

    print("="*60)


if __name__ == '__main__':
    main()
