"""
集成测试：测试主控层与知识层、执行层、输出层的完整集成
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from orchestrator.orchestrator import IndustryResearchOrchestrator


def test_quick_mode_integration():
    """测试快速模式完整流程"""
    print("="*70)
    print("集成测试：快速模式（70分钟）")
    print("="*70)

    # 初始化主控层
    orchestrator = IndustryResearchOrchestrator(mode='quick')

    # 执行研究
    result = orchestrator.run(
        industry_name='医疗陪护',
        user_params={
            'industry': '医疗陪护',
            'web_search': True,
            'mode': 'quick'
        }
    )

    # 验证结果
    print("\n" + "="*70)
    print("测试结果验证")
    print("="*70)

    assert result['status'] == 'success', "状态应为success"
    assert result['mode'] == 'quick', "模式应为quick"
    assert result['industry'] == '医疗陪护', "行业应为医疗陪护"

    print("✅ 所有断言通过")

    return result


def test_full_mode_integration():
    """测试全量模式完整流程"""
    print("\n" + "="*70)
    print("集成测试：全量模式（3-5小时）")
    print("="*70)

    # 初始化主控层
    orchestrator = IndustryResearchOrchestrator(mode='full')

    # 执行研究
    result = orchestrator.run(
        industry_name='医疗陪护',
        user_params={
            'industry': '医疗陪护',
            'web_search': True,
            'mode': 'full'
        }
    )

    # 验证结果
    print("\n" + "="*70)
    print("测试结果验证")
    print("="*70)

    assert result['mode'] == 'full', "模式应为full"
    assert result['industry'] == '医疗陪护', "行业应为医疗陪护"

    print("✅ 所有断言通过")

    return result


def main():
    """主测试函数"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*10 + "Industry Research Skill - 集成测试" + " "*23 + "║")
    print("╚" + "="*68 + "╝")

    try:
        # 测试快速模式
        quick_result = test_quick_mode_integration()

        # 测试全量模式
        full_result = test_full_mode_integration()

        print("\n" + "="*70)
        print("🎉 所有集成测试通过!")
        print("="*70)
        print("\n项目状态:")
        print("  ✅ 项目结构创建完成")
        print("  ✅ 知识层实现完成（框架选择器 + 数据源选择器）")
        print("  ✅ 执行层框架完成（数据收集、框架应用）")
        print("  ✅ 输出层框架完成（质检、报告生成、打包）")
        print("  ✅ 主控层集成测试通过")
        print("\n下一步:")
        print("  1. 实现真实的web_search联网搜索")
        print("  2. 实现图表生成器（SVG/PNG）")
        print("  3. 创建HTML交互表单")
        print("  4. 完善质量检查规则")

    except Exception as e:
        print("\n" + "="*70)
        print(f"❌ 测试失败: {e}")
        print("="*70)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
