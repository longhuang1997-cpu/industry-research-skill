"""
Web搜索集成模块 - 为研究引擎提供真实数据支持

设计原则：
1. 依赖Claude Code的WebSearch工具（不需要额外API）
2. 搜索结果要求溯源（URL + 来源）
3. 失败时优雅降级（回退到LLM记忆，但明确标注）
"""

from typing import List, Dict, Optional
import json


class WebSearchIntegration:
    """Web搜索集成 - Claude Code环境下的实现"""

    def __init__(self, use_web_search: bool = True):
        """
        初始化搜索集成

        Args:
            use_web_search: 是否启用Web搜索（False时回退到LLM记忆）
        """
        self.use_web_search = use_web_search
        self.search_history = []  # 记录所有搜索历史（用于溯源）

    def search_for_dimension(self, industry: str, dimension: str, specific_query: Optional[str] = None) -> Dict:
        """
        为特定分析维度执行搜索

        Args:
            industry: 行业名称
            dimension: 分析维度（如"政策环境"、"市场规模"）
            specific_query: 自定义查询（如果为None，自动生成）

        Returns:
            {
                'query': '实际搜索词',
                'results': [...],  # 搜索结果
                'sources': [...],  # 来源URL
                'method': 'web_search' or 'llm_fallback'
            }
        """
        # 生成搜索查询
        query = specific_query or self._generate_query(industry, dimension)

        if not self.use_web_search:
            return self._fallback_response(query, "Web搜索已禁用")

        try:
            # 调用Claude Code的WebSearch工具
            # 注意：这里需要通过tool调用，不是直接代码调用
            search_instruction = self._create_search_instruction(query)

            return {
                'query': query,
                'instruction': search_instruction,
                'method': 'web_search_required',
                'note': '需要调用WebSearch工具执行此搜索'
            }

        except Exception as e:
            return self._fallback_response(query, f"搜索失败: {str(e)}")

    def _generate_query(self, industry: str, dimension: str) -> str:
        """根据维度生成搜索查询"""
        query_templates = {
            '行业画像': f'{industry} 行业概况 发展现状',
            '政策环境': f'{industry} 政策 监管 支持政策',
            '市场规模': f'{industry} 市场规模 增长率 统计数据',
            '商业模式': f'{industry} 商业模式 盈利模式 案例',
            '竞争格局': f'{industry} 竞争格局 市场份额 主要玩家',
            '进入壁垒': f'{industry} 进入门槛 壁垒 牌照',
            '风险分析': f'{industry} 风险 挑战 问题',
            '战略建议': f'{industry} 投资机会 战略建议'
        }
        return query_templates.get(dimension, f'{industry} {dimension}')

    def _create_search_instruction(self, query: str) -> str:
        """创建搜索指令（给调用者）"""
        return f"请使用WebSearch工具搜索: {query}\n要求: 返回前5条结果，包含URL来源"

    def _fallback_response(self, query: str, reason: str) -> Dict:
        """降级响应（无法搜索时）"""
        return {
            'query': query,
            'method': 'llm_fallback',
            'reason': reason,
            'warning': '⚠️ 以下内容基于LLM训练记忆，非实时数据，请谨慎使用'
        }

    def format_sources(self, search_results: List[Dict]) -> str:
        """格式化数据来源（用于报告末尾）"""
        if not search_results:
            return "⚠️ 本报告未使用实时搜索数据，内容基于AI模型训练记忆"

        sources = []
        for i, result in enumerate(search_results, 1):
            if result.get('method') == 'web_search':
                sources.append(f"{i}. [{result.get('title', 'N/A')}]({result.get('url', '#')})")

        if not sources:
            return "⚠️ 本报告未使用实时搜索数据，内容基于AI模型训练记忆"

        return "## 数据来源\n\n" + "\n".join(sources)


class SearchAugmentedPrompt:
    """搜索增强的Prompt生成器"""

    @staticmethod
    def create_research_prompt(industry: str, dimension: str, search_context: Dict) -> str:
        """
        生成搜索增强的研究Prompt

        Args:
            industry: 行业名称
            dimension: 分析维度
            search_context: 搜索结果上下文

        Returns:
            增强后的Prompt（包含搜索结果）
        """
        base_prompt = f"""
你是一位资深行业分析师，正在研究【{industry}】行业的【{dimension}】。

## 任务要求
1. 基于提供的搜索结果进行分析（优先使用真实数据）
2. 所有数字必须标注来源（[来源X]）
3. 如果搜索结果不足，明确说明哪些是推测

## 搜索结果
"""

        # 添加搜索结果（如果有）
        if search_context.get('method') == 'web_search' and search_context.get('results'):
            for i, result in enumerate(search_context['results'], 1):
                base_prompt += f"\n[来源{i}] {result.get('title', 'N/A')}\n"
                base_prompt += f"URL: {result.get('url', 'N/A')}\n"
                base_prompt += f"内容摘要: {result.get('snippet', 'N/A')}\n"
        else:
            base_prompt += f"\n⚠️ 搜索结果不可用（原因: {search_context.get('reason', '未知')}）\n"
            base_prompt += "请基于你的知识进行分析，但必须在报告开头明确标注「本部分未使用实时数据」\n"

        base_prompt += f"""

## 输出要求
- 格式: Markdown
- 长度: 300-500字
- 必须包含: 具体数字、案例、来源标注
- 分析框架: {SearchAugmentedPrompt._get_framework(dimension)}
"""

        return base_prompt

    @staticmethod
    def _get_framework(dimension: str) -> str:
        """获取维度对应的分析框架"""
        frameworks = {
            '政策环境': 'PEST-P框架',
            '市场规模': 'Top-down + Bottom-up估算',
            '商业模式': '四方决策链 + LTV/CAC',
            '竞争格局': 'Porter五力模型',
            '进入壁垒': '五大壁垒分析',
            '风险分析': 'PESTEL风险矩阵'
        }
        return frameworks.get(dimension, '结构化分析')


# ==================== 使用示例 ====================

def example_usage():
    """使用示例"""
    search = WebSearchIntegration(use_web_search=True)

    # 1. 为"政策环境"维度生成搜索
    search_task = search.search_for_dimension(
        industry="医疗陪护",
        dimension="政策环境"
    )
    print(f"搜索指令: {search_task['instruction']}")

    # 2. 假设拿到了搜索结果（由调用者执行WebSearch后填入）
    search_results = {
        'query': '医疗陪护 政策',
        'method': 'web_search',
        'results': [
            {'title': '国家卫健委发布陪护服务规范', 'url': 'http://...', 'snippet': '...'},
        ]
    }

    # 3. 生成增强Prompt
    prompt = SearchAugmentedPrompt.create_research_prompt(
        industry="医疗陪护",
        dimension="政策环境",
        search_context=search_results
    )
    print(f"增强Prompt: {prompt}")


if __name__ == "__main__":
    example_usage()
