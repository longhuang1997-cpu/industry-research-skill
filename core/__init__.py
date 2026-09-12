"""
Industry Research Skill - 核心模块

重构后的精简架构（2026-09-12）：
- ResearchEngine: 统一研究引擎（意图理解+工作流+AI分析+质量检查）
- Orchestrator: 精简主控层（编排+报告生成）
"""

from .research_engine import ResearchEngine
from .orchestrator import Orchestrator

__all__ = ['ResearchEngine', 'Orchestrator']
