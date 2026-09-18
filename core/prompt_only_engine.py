"""
Prompt-Only Research Engine - 零API完整分析引擎

核心理念：
- 不调用任何外部API
- 返回结构化的Prompt给调用方Agent
- Agent自己执行分析，填充内容
- Skill只负责方法论框架+流程控制

用法：
    engine = PromptOnlyEngine()
    prompts = engine.get_analysis_prompts(industry='医疗陪护', dimensions=['政策环境', '市场规模'])

    # 调用方Agent逐个执行prompt，获得分析内容
    for prompt_info in prompts:
        content = your_agent.analyze(prompt_info['prompt'])
        results.append({
            'dimension': prompt_info['dimension'],
            'content': content
        })
"""

from pathlib import Path
from typing import Dict, List, Optional
from core.research_engine import ResearchEngine


class PromptOnlyEngine:
    """
    Prompt-Only 研究引擎

    不调用API，只返回Prompt给调用方Agent执行
    """

    def __init__(self):
        """初始化（不需要API密钥）"""
        # 复用ResearchEngine的方法论部分
        self.base_engine = ResearchEngine()

    def get_analysis_prompts(self,
                            industry: str,
                            dimensions: List[str] = None,
                            research_type: str = "行业分析") -> List[Dict]:
        """
        获取完整的分析Prompt列表

        Args:
            industry: 行业名称
            dimensions: 分析维度列表（None则使用默认）
            research_type: 研究类型

        Returns:
            [
                {
                    'dimension': '政策环境',
                    'time': 8,
                    'prompt': '完整的分析Prompt',
                    'hypothesis': '核心假设',
                    'evidence_needed': {...},
                    'conclusion_format': '结论格式要求',
                    'context': {}  # 上下文（依赖的前序结果）
                },
                ...
            ]
        """
        # 生成工作流
        if dimensions is None:
            dimensions = ['政策环境', '市场规模', '商业模式']

        workflow_result = self.base_engine.create_workflow(
            dimensions=dimensions,
            research_type=research_type
        )

        workflow = workflow_result['workflow']

        # 为每个步骤生成Prompt
        prompts = []
        context = {}

        for step in workflow:
            dimension = step['name']
            template_name = step.get('prompt_template')

            # 生成Prompt（复用ResearchEngine的_get_prompt方法）
            prompt = self.base_engine._get_prompt(
                template_name=template_name,
                industry=industry,
                context=context
            )

            prompt_info = {
                'dimension': dimension,
                'time': step['time'],
                'prompt': prompt,
                'hypothesis': step.get('hypothesis', ''),
                'evidence_needed': step.get('evidence_needed', {}),
                'conclusion_format': step.get('conclusion_format', ''),
                'context': dict(context),  # 传递上下文快照
                'needs_internal_data': step.get('needs_internal_data', False),
                'internal_data_desc': step.get('internal_data_desc', '')
            }

            prompts.append(prompt_info)

            # 更新上下文占位符（调用方需要填充实际内容）
            context[dimension] = f"[待填充: {dimension}的分析结果]"

        return prompts

    def get_single_dimension_prompt(self,
                                   industry: str,
                                   dimension: str,
                                   context: Dict = None) -> Dict:
        """
        获取单个维度的分析Prompt

        Args:
            industry: 行业名称
            dimension: 分析维度
            context: 上下文（前序分析结果）

        Returns:
            {
                'dimension': str,
                'prompt': str,
                'hypothesis': str,
                'evidence_needed': Dict,
                'conclusion_format': str
            }
        """
        if dimension not in self.base_engine.DIMENSIONS:
            raise ValueError(f"未知维度: {dimension}")

        template_name = self.base_engine.DIMENSIONS[dimension].get('prompt_template')

        # 生成Prompt
        prompt = self.base_engine._get_prompt(
            template_name=template_name,
            industry=industry,
            context=context or {}
        )

        # 获取假设-证据-结论框架
        research_type = "行业分析"  # 默认类型，可扩展
        framework = self.base_engine._generate_hypothesis_evidence_conclusion(
            research_type=research_type,
            dimension=dimension
        )

        return {
            'dimension': dimension,
            'prompt': prompt,
            'hypothesis': framework.get('hypothesis', ''),
            'evidence_needed': framework.get('evidence_needed', {}),
            'conclusion_format': framework.get('conclusion_format', ''),
            'needs_internal_data': framework.get('needs_internal_data', False),
            'internal_data_desc': framework.get('internal_data_desc', '')
        }

    def create_workflow(self,
                       dimensions: List[str],
                       research_type: str = "行业分析") -> Dict:
        """
        创建工作流（复用ResearchEngine的方法）

        Returns:
            与ResearchEngine.create_workflow相同的结构
        """
        return self.base_engine.create_workflow(
            dimensions=dimensions,
            research_type=research_type
        )

    def check_quality(self, results: List[Dict]) -> Dict:
        """
        质量检查（复用ResearchEngine的方法）

        Args:
            results: [{'dimension': str, 'content': str, 'quality_score': float}, ...]

        Returns:
            {'passed': bool, 'issues': [], 'suggestions': [], 'avg_quality': float}
        """
        return self.base_engine.check_quality(results)

    def assess_content_quality(self, content: str) -> float:
        """
        评估内容质量（复用ResearchEngine的_assess_quality方法）

        Args:
            content: 分析内容

        Returns:
            质量分数 (0.0 - 1.0)
        """
        return self.base_engine._assess_quality(content)


# 便捷函数
def get_prompts_for_industry(industry: str,
                             dimensions: List[str] = None,
                             research_type: str = "行业分析") -> List[Dict]:
    """
    快速获取行业研究的所有Prompt

    用法:
        prompts = get_prompts_for_industry('医疗陪护', ['政策环境', '市场规模'])
        for p in prompts:
            print(f"维度: {p['dimension']}")
            print(f"Prompt: {p['prompt']}")
    """
    engine = PromptOnlyEngine()
    return engine.get_analysis_prompts(industry, dimensions, research_type)
