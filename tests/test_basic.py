"""
测试框架选择器和数据源选择器的基础功能
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from knowledge.frameworks.framework_selector import FrameworkSelector
from knowledge.data_sources.data_source_selector import DataSourceSelector


def test_framework_selector():
    """测试框架选择器"""
    print("="*70)
    print("测试1: 框架选择器")
    print("="*70)

    selector = FrameworkSelector()

    # 测试已知行业
    print("\n测试: 医疗陪护（已知行业）")
    print("-"*70)
    frameworks = selector.select_frameworks('医疗陪护')

    print("\n选择的框架:")
    for i, fw in enumerate(frameworks, 1):
        print(f"  {i}. {fw['name']} - 权重{fw['weight']}")
        print(f"     关注点: {fw['focus']}")

    print("\n关键问题:")
    questions = selector.get_key_questions('医疗陪护')
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")

    # 测试未知行业
    print("\n" + "-"*70)
    print("测试: 月子中心（未知行业，需要用户回答）")
    print("-"*70)
    user_input = {
        'policy_sensitivity': 'high',
        'payment_model': '混合'
    }
    frameworks = selector.select_frameworks('月子中心', user_input)


def test_data_source_selector():
    """测试数据源选择器"""
    print("\n" + "="*70)
    print("测试2: 数据源选择器")
    print("="*70)

    selector = DataSourceSelector()

    print("\n测试: 医疗陪护")
    print("-"*70)

    # 测试搜索关键词生成
    keywords = selector.generate_search_keywords('医疗陪护')

    print("\n搜索关键词清单:")
    for i, kw in enumerate(keywords[:5], 1):  # 只显示前5个
        print(f"  {i}. [Tier {kw['tier']}] {kw['keyword']}")
    if len(keywords) > 5:
        print(f"  ... 共{len(keywords)}个关键词")

    # 测试Tier 1数据源
    print("\nTier 1数据源:")
    sources = selector.get_tier1_sources('医疗陪护')
    for source in sources:
        print(f"  - {source['name']}")
        print(f"    URL: {source['url']}")
        if 'data_types' in source:
            print(f"    数据类型: {', '.join(source['data_types'])}")


def main():
    """主测试函数"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "Industry Research Skill - 单元测试" + " "*18 + "║")
    print("╚" + "="*68 + "╝")

    try:
        # 测试框架选择器
        test_framework_selector()

        # 测试数据源选择器
        test_data_source_selector()

        print("\n" + "="*70)
        print("✅ 所有测试通过!")
        print("="*70)

    except Exception as e:
        print("\n" + "="*70)
        print(f"❌ 测试失败: {e}")
        print("="*70)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
