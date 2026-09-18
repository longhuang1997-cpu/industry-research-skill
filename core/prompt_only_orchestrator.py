"""
Prompt-Only Orchestrator - 零API完整分析主控层

核心理念：
- Skill负责方法论框架+流程控制+报告生成
- 调用方Agent负责执行分析Prompt，填充内容
- 不依赖任何外部API

使用场景：
1. WorkBuddy/Claude Code在对话中分析
2. 其他Agent集成Industry Research方法论
3. 企业内部AI能力沉淀

用法示例：
    from core.prompt_only_orchestrator import PromptOnlyOrchestrator

    # 初始化
    orch = PromptOnlyOrchestrator()

    # 获取分析任务清单
    tasks = orch.get_research_tasks('医疗陪护', dimensions=['政策环境', '市场规模'])

    # Agent逐个执行
    results = []
    for task in tasks:
        content = your_agent.analyze(task['prompt'])
        results.append({
            'dimension': task['dimension'],
            'content': content,
            'quality_score': task['assess_quality'](content)
        })

    # 生成报告
    report = orch.generate_report('医疗陪护', results)
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Callable
from datetime import datetime

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))


class PromptOnlyOrchestrator:
    """
    Prompt-Only主控层 - 零API完整分析

    职责：
    1. 生成研究任务清单（Prompt列表）
    2. 协调调用方Agent执行分析
    3. 质量检查
    4. 生成专业报告
    """

    def __init__(self, mode='standard'):
        """
        初始化

        Args:
            mode: 'quick'/'standard'/'deep' 研究深度
        """
        self.mode = mode
        self.skill_root = SKILL_ROOT

        print(f"[PromptOnlyOrchestrator] 初始化 {mode} 模式（零API）")

        # 初始化Prompt引擎
        from core.prompt_only_engine import PromptOnlyEngine
        self.engine = PromptOnlyEngine()

        # 初始化报告生成器
        from output.professional_report_generator import ProfessionalReportGenerator
        self.report_generator = ProfessionalReportGenerator()

    def get_research_tasks(self,
                          industry: str,
                          dimensions: List[str] = None,
                          research_type: str = "行业分析") -> List[Dict]:
        """
        获取研究任务清单

        Args:
            industry: 行业名称
            dimensions: 分析维度列表
            research_type: 研究类型

        Returns:
            [
                {
                    'step': 1,
                    'total': 5,
                    'dimension': '政策环境',
                    'time': 8,
                    'prompt': '完整的分析Prompt',
                    'hypothesis': '核心假设',
                    'evidence_needed': {...},
                    'conclusion_format': '结论格式',
                    'needs_internal_data': False,
                    'internal_data_desc': '',
                    'assess_quality': Callable  # 质量评估函数
                },
                ...
            ]
        """
        print(f"\n{'='*60}")
        print(f"生成研究任务: {industry}")
        print(f"{'='*60}\n")

        # 获取Prompt列表
        prompts = self.engine.get_analysis_prompts(
            industry=industry,
            dimensions=dimensions,
            research_type=research_type
        )

        # 封装为任务清单
        tasks = []
        total = len(prompts)

        for i, prompt_info in enumerate(prompts, 1):
            task = {
                'step': i,
                'total': total,
                'dimension': prompt_info['dimension'],
                'time': prompt_info['time'],
                'prompt': prompt_info['prompt'],
                'hypothesis': prompt_info['hypothesis'],
                'evidence_needed': prompt_info['evidence_needed'],
                'conclusion_format': prompt_info['conclusion_format'],
                'needs_internal_data': prompt_info['needs_internal_data'],
                'internal_data_desc': prompt_info['internal_data_desc'],
                'context': prompt_info['context'],
                # 附加质量评估函数
                'assess_quality': lambda content: self.engine.assess_content_quality(content)
            }
            tasks.append(task)

            print(f"[任务 {i}/{total}] {task['dimension']}")
            print(f"  预计: {task['time']}分钟")
            if task['needs_internal_data']:
                print(f"  [WARN]  需要内部数据: {task['internal_data_desc']}")
            print()

        print(f"{'='*60}")
        print(f"共生成 {total} 个研究任务")
        print(f"{'='*60}\n")

        return tasks

    def generate_report(self,
                       industry: str,
                       analysis_results: List[Dict],
                       export_formats: List[str] = None) -> Dict:
        """
        生成专业报告

        Args:
            industry: 行业名称
            analysis_results: 分析结果列表
                [
                    {
                        'dimension': '政策环境',
                        'content': '分析内容...',
                        'quality_score': 0.85,
                        'counter_evidences': []  # 可选
                    },
                    ...
                ]
            export_formats: 导出格式列表 ['word', 'markdown']

        Returns:
            {
                'status': 'success',
                'path': '报告路径',
                'quality': {...},
                'exported_files': {...}
            }
        """
        print(f"\n{'='*60}")
        print(f"生成报告: {industry}")
        print(f"{'='*60}\n")

        try:
            # Step 1: 质量检查
            print("[Step 1] 质量检查...")
            quality_check = self.engine.check_quality(analysis_results)
            print(f"  平均质量分: {quality_check['avg_quality']:.2f}")

            if quality_check['passed']:
                print(f"  [OK] 质量检查通过")
            else:
                print(f"  [WARN]  质量问题: {', '.join(quality_check['issues'])}")
                for suggestion in quality_check['suggestions']:
                    print(f"     建议: {suggestion}")

            # Step 2: 生成HTML报告
            print("\n[Step 2] 生成HTML报告...")
            report_data = {
                'industry': industry,
                'mode': self.mode,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'analysis_results': analysis_results,
                'quality_check': quality_check
            }

            report_path = self.report_generator.generate_report(
                industry=industry,
                research_data=report_data,
                report_type='full'
            )
            print(f"  [OK] HTML报告: {report_path}")

            # Step 3: 多格式导出（可选）
            exported_files = {}
            if export_formats:
                print("\n[Step 3] 导出其他格式...")
                from output.report_exporter import ReportExporter
                exporter = ReportExporter()

                for fmt in export_formats:
                    try:
                        output_path = exporter.export_report(report_path, fmt)
                        exported_files[fmt] = output_path
                        print(f"  [OK] {fmt.upper()}: {output_path}")
                    except Exception as e:
                        print(f"  [WARN]  {fmt.upper()}导出失败: {e}")

            print(f"\n{'='*60}")
            print(f"[OK] 报告生成完成!")
            print(f"{'='*60}\n")

            result = {
                'status': 'success',
                'industry': industry,
                'mode': self.mode,
                'path': report_path,
                'quality': quality_check,
                'analysis_results': analysis_results
            }

            if exported_files:
                result['exported_files'] = exported_files

            return result

        except Exception as e:
            print(f"\n{'='*60}")
            print(f"[ERROR] 报告生成失败")
            print(f"{'='*60}")
            print(f"错误: {type(e).__name__}: {str(e)}\n")

            return {
                'status': 'error',
                'industry': industry,
                'error': str(e),
                'error_type': type(e).__name__
            }

    def quick_start(self, industry: str) -> str:
        """
        快速开始（纯Prompt模式，不执行分析）

        用于：
        - 快速查看研究框架
        - 获取Prompt模板
        - 方法论演示

        Args:
            industry: 行业名称

        Returns:
            summary: 任务清单摘要文本
        """
        tasks = self.get_research_tasks(industry)

        summary_lines = [
            f"# {industry} - 研究任务清单",
            "",
            f"共 {len(tasks)} 个分析任务，预计总时间: {sum(t['time'] for t in tasks)} 分钟",
            "",
            "## 任务列表",
            ""
        ]

        for task in tasks:
            summary_lines.append(f"### 任务 {task['step']}: {task['dimension']}")
            summary_lines.append(f"- **预计时间**: {task['time']}分钟")
            summary_lines.append(f"- **假设**: {task['hypothesis']}")
            summary_lines.append(f"- **结论格式**: {task['conclusion_format']}")

            if task['needs_internal_data']:
                summary_lines.append(f"- [WARN] **需要内部数据**: {task['internal_data_desc']}")

            summary_lines.append("")
            summary_lines.append("**Prompt预览**:")
            summary_lines.append("```")
            summary_lines.append(task['prompt'][:200] + "..." if len(task['prompt']) > 200 else task['prompt'])
            summary_lines.append("```")
            summary_lines.append("")

        summary = "\n".join(summary_lines)
        return summary


# 便捷函数
def quick_research_guide(industry: str, dimensions: List[str] = None) -> str:
    """
    快速生成研究指南（纯Prompt，不执行分析）

    用法:
        guide = quick_research_guide('医疗陪护', ['政策环境', '市场规模'])
        print(guide)
    """
    orch = PromptOnlyOrchestrator()
    return orch.quick_start(industry)
