"""
零API完整分析 - 使用示例

演示如何在不调用外部API的情况下，完成完整的行业研究分析。

核心思路：
1. Skill生成分析任务清单（Prompt + 方法论框架）
2. 调用方Agent（如WorkBuddy）执行每个Prompt
3. Skill收集结果，进行质量检查
4. Skill生成专业报告（HTML/Word/Markdown）

适用场景：
- Claude Code在对话中完成研究
- 其他Agent集成Industry Research方法论
- 企业内部AI能力沉淀
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))


def example_1_get_tasks():
    """
    示例1: 获取研究任务清单

    返回: 任务列表，包含每个维度的Prompt
    """
    print("="*80)
    print("示例1: 获取研究任务清单")
    print("="*80)

    from core.prompt_only_orchestrator import PromptOnlyOrchestrator

    # 初始化
    orch = PromptOnlyOrchestrator(mode='quick')

    # 获取任务清单
    tasks = orch.get_research_tasks(
        industry='医疗陪护',
        dimensions=['政策环境', '市场规模', '商业模式']
    )

    # 打印任务清单
    print("\n任务清单摘要:")
    print(f"共 {len(tasks)} 个任务\n")

    for task in tasks:
        print(f"任务 {task['step']}/{task['total']}: {task['dimension']}")
        print(f"  预计时间: {task['time']}分钟")
        print(f"  假设: {task['hypothesis'][:80]}...")
        print(f"  Prompt长度: {len(task['prompt'])}字符")
        print()

    return tasks


def example_2_manual_execution(tasks):
    """
    示例2: 手动执行分析（模拟Agent填充内容）

    在真实场景中，这里应该是：
        content = your_agent.analyze(task['prompt'])

    这里用Mock内容演示流程
    """
    print("="*80)
    print("示例2: 手动执行分析")
    print("="*80)

    results = []

    for task in tasks:
        print(f"\n[任务 {task['step']}/{task['total']}] 分析 {task['dimension']}...")

        # [REAL] 真实场景：调用Agent执行Prompt
        # content = your_agent.analyze(task['prompt'])

        # [MOCK] 示例：用Mock内容演示
        mock_content = f"""
# {task['dimension']}分析

{task['hypothesis']}

## 核心发现
1. 数据点1: 市场规模约500亿元（2024年）
2. 数据点2: 年增长率15-20%
3. 数据点3: 政策支持力度持续加大

## 详细论证
（这里是详细的分析内容，包含数据支撑和案例...）

## 结论
{task['conclusion_format']}
"""

        # 评估质量
        quality_score = task['assess_quality'](mock_content)

        result = {
            'dimension': task['dimension'],
            'content': mock_content,
            'quality_score': quality_score
        }
        results.append(result)

        print(f"  [OK] 完成 (质量分: {quality_score:.2f})")

    return results


def example_3_generate_report(industry, results):
    """
    示例3: 生成专业报告

    Skill负责报告生成，不需要Agent参与
    """
    print("\n" + "="*80)
    print("示例3: 生成专业报告")
    print("="*80)

    from core.prompt_only_orchestrator import PromptOnlyOrchestrator

    orch = PromptOnlyOrchestrator()

    # 生成报告（支持多格式导出）
    report_result = orch.generate_report(
        industry=industry,
        analysis_results=results,
        export_formats=['word', 'markdown']  # 可选：导出Word和Markdown
    )

    if report_result['status'] == 'success':
        print(f"\n[OK] 报告生成成功!")
        print(f"  HTML: {report_result['path']}")

        if 'exported_files' in report_result:
            for fmt, path in report_result['exported_files'].items():
                print(f"  {fmt.upper()}: {path}")

        print(f"\n质量摘要:")
        print(f"  平均质量分: {report_result['quality']['avg_quality']:.2f}")
        print(f"  检查结果: {'通过 [OK]' if report_result['quality']['passed'] else '有问题 [WARN]'}")

    return report_result


def example_4_quick_guide():
    """
    示例4: 快速生成研究指南（不执行分析）

    用于：
    - 快速查看研究框架
    - 获取Prompt模板
    - 方法论演示
    """
    print("\n" + "="*80)
    print("示例4: 快速生成研究指南")
    print("="*80)

    from core.prompt_only_orchestrator import quick_research_guide

    guide = quick_research_guide(
        industry='智能制造',
        dimensions=['政策环境', '技术趋势']
    )

    # 保存到桌面
    desktop = Path.home() / "Desktop"
    guide_file = desktop / "research_guide_智能制造.md"

    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide)

    print(f"\n[OK] 研究指南已生成: {guide_file}")
    print(f"   大小: {len(guide)}字符\n")


def example_5_workbuddy_integration():
    """
    示例5: WorkBuddy集成示例（伪代码）

    展示如何在Claude Code对话中使用
    """
    print("\n" + "="*80)
    print("示例5: WorkBuddy集成示例（伪代码）")
    print("="*80)

    pseudo_code = """
# WorkBuddy使用Industry Research Skill的典型流程

def workbuddy_research_industry(industry: str, user_question: str):
    '''
    用户问: "帮我研究医疗陪护行业"
    '''

    # Step 1: 获取研究任务清单
    from core.prompt_only_orchestrator import PromptOnlyOrchestrator
    orch = PromptOnlyOrchestrator()

    tasks = orch.get_research_tasks(
        industry=industry,
        dimensions=['政策环境', '市场规模', '商业模式']  # 根据用户问题智能选择
    )

    # Step 2: 在对话中逐个分析（用我自己的能力）
    results = []
    for task in tasks:
        # 用我（WorkBuddy）的联网检索+分析能力执行Prompt
        content = my_analyze_with_web_search(
            prompt=task['prompt'],
            hypothesis=task['hypothesis'],
            evidence_needed=task['evidence_needed']
        )

        # 评估质量
        quality_score = task['assess_quality'](content)

        results.append({
            'dimension': task['dimension'],
            'content': content,
            'quality_score': quality_score
        })

        # 在对话中实时展示进度
        print(f"[OK] 完成 {task['dimension']} 分析")

    # Step 3: 询问用户是否生成报告
    user_confirm = ask_user("是否生成专业报告（HTML/Word）?")

    if user_confirm:
        report = orch.generate_report(
            industry=industry,
            analysis_results=results,
            export_formats=['word']
        )
        print(f"[OK] 报告已生成: {report['path']}")
    else:
        # 直接在对话中呈现分析结果
        for result in results:
            print(f"## {result['dimension']}")
            print(result['content'])
            print()
"""

    print(pseudo_code)


def main():
    """
    主函数：运行所有示例
    """
    print("\n" + "="*80)
    print("零API完整分析 - 使用示例")
    print("="*80 + "\n")

    # 示例1: 获取任务清单
    tasks = example_1_get_tasks()

    # 示例2: 手动执行分析
    results = example_2_manual_execution(tasks)

    # 示例3: 生成专业报告
    report = example_3_generate_report('医疗陪护', results)

    # 示例4: 快速生成研究指南
    example_4_quick_guide()

    # 示例5: WorkBuddy集成示例
    example_5_workbuddy_integration()

    print("\n" + "="*80)
    print("所有示例运行完成!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
