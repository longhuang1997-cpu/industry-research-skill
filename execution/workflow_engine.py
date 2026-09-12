"""
灵活工作流引擎：支持用户自定义研究深度和路径

特性:
1. 多层次工作流（快速/标准/深度/自定义）
2. 可选择的分析维度
3. 动态调整研究深度
4. 进度可视化
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class ResearchDepth(Enum):
    """研究深度级别"""
    QUICK = "quick"           # 10分钟快速洞察
    STANDARD = "standard"     # 30分钟标准研究
    DEEP = "deep"            # 60分钟深度研究
    CUSTOM = "custom"        # 自定义研究路径


class AnalysisDimension(Enum):
    """分析维度"""
    POLICY = "政策环境"
    MARKET_SIZE = "市场规模"
    BUSINESS_MODEL = "商业模式"
    COMPETITION = "竞争格局"
    ENTRY_BARRIERS = "进入壁垒"
    SUPPLY_CHAIN = "产业链分析"
    RISK_ANALYSIS = "风险分析"
    OPPORTUNITIES = "机会识别"


@dataclass
class WorkflowStep:
    """工作流步骤"""
    name: str
    dimension: AnalysisDimension
    estimated_time: int  # 预计耗时（分钟）
    required: bool      # 是否必选
    dependencies: List[str]  # 依赖的步骤


@dataclass
class WorkflowConfig:
    """工作流配置"""
    depth: ResearchDepth
    dimensions: List[AnalysisDimension]
    include_charts: bool
    include_data_tables: bool
    generate_pdf: bool


class WorkflowEngine:
    """
    灵活工作流引擎

    支持多种研究深度和自定义路径
    """

    def __init__(self):
        """初始化工作流引擎"""
        self.available_steps = self._define_available_steps()
        self.predefined_workflows = self._define_predefined_workflows()

    def _define_available_steps(self) -> Dict[str, WorkflowStep]:
        """定义所有可用的研究步骤"""
        return {
            "industry_profile": WorkflowStep(
                name="行业画像",
                dimension=AnalysisDimension.MARKET_SIZE,
                estimated_time=2,
                required=True,
                dependencies=[]
            ),
            "policy_analysis": WorkflowStep(
                name="政策环境深度分析",
                dimension=AnalysisDimension.POLICY,
                estimated_time=8,
                required=False,
                dependencies=["industry_profile"]
            ),
            "market_sizing": WorkflowStep(
                name="市场规模测算",
                dimension=AnalysisDimension.MARKET_SIZE,
                estimated_time=8,
                required=False,
                dependencies=["industry_profile"]
            ),
            "business_model": WorkflowStep(
                name="商业模式拆解",
                dimension=AnalysisDimension.BUSINESS_MODEL,
                estimated_time=10,
                required=False,
                dependencies=["market_sizing"]
            ),
            "competition": WorkflowStep(
                name="竞争格局分析",
                dimension=AnalysisDimension.COMPETITION,
                estimated_time=8,
                required=False,
                dependencies=["market_sizing"]
            ),
            "entry_barriers": WorkflowStep(
                name="进入壁垒评估",
                dimension=AnalysisDimension.ENTRY_BARRIERS,
                estimated_time=6,
                required=False,
                dependencies=["competition"]
            ),
            "supply_chain": WorkflowStep(
                name="产业链分析",
                dimension=AnalysisDimension.SUPPLY_CHAIN,
                estimated_time=10,
                required=False,
                dependencies=["business_model"]
            ),
            "risk_analysis": WorkflowStep(
                name="风险分析",
                dimension=AnalysisDimension.RISK_ANALYSIS,
                estimated_time=6,
                required=False,
                dependencies=["policy_analysis", "market_sizing"]
            ),
            "opportunities": WorkflowStep(
                name="机会识别",
                dimension=AnalysisDimension.OPPORTUNITIES,
                estimated_time=8,
                required=False,
                dependencies=["competition", "entry_barriers"]
            )
        }

    def _define_predefined_workflows(self) -> Dict[ResearchDepth, List[str]]:
        """定义预设工作流"""
        return {
            ResearchDepth.QUICK: [
                "industry_profile",
                "policy_analysis",
                "market_sizing"
            ],
            ResearchDepth.STANDARD: [
                "industry_profile",
                "policy_analysis",
                "market_sizing",
                "business_model",
                "competition"
            ],
            ResearchDepth.DEEP: [
                "industry_profile",
                "policy_analysis",
                "market_sizing",
                "business_model",
                "competition",
                "entry_barriers",
                "supply_chain",
                "risk_analysis",
                "opportunities"
            ]
        }

    def create_workflow(self, config: WorkflowConfig) -> List[WorkflowStep]:
        """
        创建工作流

        Args:
            config: 工作流配置

        Returns:
            steps: 工作流步骤列表
        """
        if config.depth != ResearchDepth.CUSTOM:
            # 使用预定义工作流
            step_names = self.predefined_workflows[config.depth]
            steps = [self.available_steps[name] for name in step_names]
        else:
            # 自定义工作流：根据用户选择的维度生成
            steps = self._build_custom_workflow(config.dimensions)

        return steps

    def _build_custom_workflow(self,
                               dimensions: List[AnalysisDimension]) -> List[WorkflowStep]:
        """
        构建自定义工作流

        Args:
            dimensions: 用户选择的分析维度

        Returns:
            steps: 工作流步骤列表
        """
        # 总是包含行业画像
        selected_steps = ["industry_profile"]

        # 根据维度添加对应步骤
        dimension_to_step = {
            AnalysisDimension.POLICY: "policy_analysis",
            AnalysisDimension.MARKET_SIZE: "market_sizing",
            AnalysisDimension.BUSINESS_MODEL: "business_model",
            AnalysisDimension.COMPETITION: "competition",
            AnalysisDimension.ENTRY_BARRIERS: "entry_barriers",
            AnalysisDimension.SUPPLY_CHAIN: "supply_chain",
            AnalysisDimension.RISK_ANALYSIS: "risk_analysis",
            AnalysisDimension.OPPORTUNITIES: "opportunities"
        }

        for dim in dimensions:
            if dim in dimension_to_step:
                step_name = dimension_to_step[dim]
                if step_name not in selected_steps:
                    selected_steps.append(step_name)

        # 解析依赖关系，确保依赖步骤也被包含
        final_steps = self._resolve_dependencies(selected_steps)

        return [self.available_steps[name] for name in final_steps]

    def _resolve_dependencies(self, step_names: List[str]) -> List[str]:
        """
        解析依赖关系

        Args:
            step_names: 步骤名称列表

        Returns:
            resolved_steps: 包含所有依赖的步骤列表（拓扑排序）
        """
        resolved = []
        visited = set()

        def visit(step_name: str):
            if step_name in visited:
                return
            visited.add(step_name)

            step = self.available_steps[step_name]
            for dep in step.dependencies:
                visit(dep)

            if step_name not in resolved:
                resolved.append(step_name)

        for name in step_names:
            visit(name)

        return resolved

    def estimate_total_time(self, steps: List[WorkflowStep]) -> int:
        """
        估算总耗时

        Args:
            steps: 工作流步骤列表

        Returns:
            total_time: 总耗时（分钟）
        """
        return sum(step.estimated_time for step in steps)

    def visualize_workflow(self, steps: List[WorkflowStep]) -> str:
        """
        可视化工作流

        Args:
            steps: 工作流步骤列表

        Returns:
            visualization: 可视化文本
        """
        total_time = self.estimate_total_time(steps)

        viz = f"\n{'='*60}\n"
        viz += f"📋 工作流概览\n"
        viz += f"{'='*60}\n\n"
        viz += f"总步骤数: {len(steps)}\n"
        viz += f"预计耗时: {total_time} 分钟\n\n"

        for i, step in enumerate(steps, 1):
            required_mark = "🔴" if step.required else "⚪"
            viz += f"{i}. {required_mark} {step.name} "
            viz += f"({step.dimension.value}, ~{step.estimated_time}分钟)\n"

            if step.dependencies:
                viz += f"   依赖: {', '.join(step.dependencies)}\n"

        viz += f"\n{'='*60}\n"

        return viz


def main():
    """测试工作流引擎"""
    print("="*60)
    print("测试: 灵活工作流引擎")
    print("="*60)

    engine = WorkflowEngine()

    # 测试1: 快速工作流
    print("\n[测试1] 快速工作流（10分钟）")
    quick_config = WorkflowConfig(
        depth=ResearchDepth.QUICK,
        dimensions=[],
        include_charts=False,
        include_data_tables=False,
        generate_pdf=False
    )
    quick_steps = engine.create_workflow(quick_config)
    print(engine.visualize_workflow(quick_steps))

    # 测试2: 标准工作流
    print("\n[测试2] 标准工作流（30分钟）")
    standard_config = WorkflowConfig(
        depth=ResearchDepth.STANDARD,
        dimensions=[],
        include_charts=True,
        include_data_tables=True,
        generate_pdf=False
    )
    standard_steps = engine.create_workflow(standard_config)
    print(engine.visualize_workflow(standard_steps))

    # 测试3: 自定义工作流
    print("\n[测试3] 自定义工作流")
    custom_config = WorkflowConfig(
        depth=ResearchDepth.CUSTOM,
        dimensions=[
            AnalysisDimension.POLICY,
            AnalysisDimension.BUSINESS_MODEL,
            AnalysisDimension.OPPORTUNITIES
        ],
        include_charts=True,
        include_data_tables=True,
        generate_pdf=True
    )
    custom_steps = engine.create_workflow(custom_config)
    print(engine.visualize_workflow(custom_steps))


if __name__ == '__main__':
    main()
