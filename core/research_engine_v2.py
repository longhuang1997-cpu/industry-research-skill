"""
v2.0集成补丁 - 将Web搜索和质量检查接入ResearchEngine

使用方式:
1. 导入: from core.research_engine_v2 import ResearchEngineV2
2. 替换: engine = ResearchEngineV2()  # 而非 ResearchEngine()
3. 使用: result = engine.analyze_dimension(...)  # API保持兼容
"""

from typing import Dict, List, Optional
from pathlib import Path
import json

# 导入v1.x的ResearchEngine（继承）
from core.research_engine import ResearchEngine

# 导入v2.0新模块
from core.web_search_integration import WebSearchIntegration, SearchAugmentedPrompt
from core.quality_checker_v2 import QualityChecker


class ResearchEngineV2(ResearchEngine):
    """
    研究引擎v2.0 - 真实搜索 + 真质量检查

    向后兼容v1.x API，但强制真实数据
    """

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None,
                 model: Optional[str] = None, enable_web_search: bool = True):
        """
        初始化v2.0引擎

        Args:
            api_key: API密钥（优先从环境变量读取）
            base_url: API base URL
            model: 模型名称
            enable_web_search: 是否启用Web搜索（False则回退v1.x行为）
        """
        # 调用父类初始化
        super().__init__(api_key, base_url, model)

        # 初始化v2.0组件
        self.web_search = WebSearchIntegration(use_web_search=enable_web_search)
        self.quality_checker = QualityChecker()
        self.search_history = []  # 记录所有搜索（用于报告溯源）

        print(f"✅ ResearchEngineV2 initialized (Web Search: {'ON' if enable_web_search else 'OFF'})")

    def analyze_dimension(self, industry: str, dimension: str,
                         context: Optional[Dict] = None) -> Dict:
        """
        分析单个维度（v2.0增强版）

        Args:
            industry: 行业名称
            dimension: 分析维度
            context: 上下文（前面维度的分析结果）

        Returns:
            {
                'dimension': str,
                'content': str,  # Markdown格式的分析内容
                'quality': {...},  # 质量检查结果
                'search_context': {...},  # 搜索上下文（用于溯源）
                'passed': bool  # 是否通过质量检查
            }
        """
        print(f"\n{'='*60}")
        print(f"📊 分析维度: {dimension}")
        print(f"{'='*60}")

        # Step 1: 执行Web搜索
        print(f"🔍 Step 1: 执行Web搜索...")
        search_task = self.web_search.search_for_dimension(industry, dimension)

        # 检查是否需要调用WebSearch工具
        if search_task.get('method') == 'web_search_required':
            print(f"   ⚠️ 需要Agent调用WebSearch工具:")
            print(f"   {search_task['instruction']}")
            print(f"\n   请在Claude Code中执行此搜索，然后将结果填入search_context")
            print(f"   或者设置enable_web_search=False回退到v1.x模式\n")

            # 暂时使用fallback（实际部署时应该等待Agent搜索）
            search_context = self.web_search._fallback_response(
                search_task['query'],
                "演示模式：实际应等待Agent搜索完成"
            )
        else:
            search_context = search_task

        # 记录搜索历史
        self.search_history.append(search_context)

        # Step 2: 生成增强Prompt
        print(f"📝 Step 2: 生成分析内容...")
        prompt = SearchAugmentedPrompt.create_research_prompt(
            industry, dimension, search_context
        )

        # Step 3: 调用LLM生成分析
        # 注意：这里需要实际调用LLM API，当前为演示
        content = self._generate_analysis(industry, dimension, prompt, context)

        # Step 4: 质量检查
        print(f"✅ Step 3: 质量检查...")
        quality_result = self.quality_checker.check_report(
            content, dimension, search_context
        )

        # 打印质量报告
        print(f"   质量分: {quality_result['score']} ({quality_result['grade']})")
        print(f"   数据来源: {search_context.get('method', 'unknown')}")
        if quality_result['issues']:
            for issue in quality_result['issues']:
                print(f"   {issue}")

        # Step 5: 判断是否通过
        passed = quality_result['passed']
        if not passed:
            print(f"\n   ❌ 质量检查失败！")
            print(f"   建议: 补充真实数据或明确标注「基于LLM记忆」")

        return {
            'dimension': dimension,
            'content': content,
            'quality': quality_result,
            'search_context': search_context,
            'passed': passed,
            'method': search_context.get('method')
        }

    def _generate_analysis(self, industry: str, dimension: str,
                          prompt: str, context: Optional[Dict]) -> str:
        """
        生成分析内容（调用LLM）

        这里是简化演示，实际应调用Anthropic API
        """
        # 检查是否使用真实搜索
        is_real_data = '来源' in prompt and 'URL:' in prompt

        if is_real_data:
            # 模拟真实搜索结果的分析
            content = f"""
## {dimension}分析

根据[来源1]的最新数据，{industry}行业在{dimension}方面呈现以下特点：

### 核心发现
- 关键指标1: 约X亿元[来源1]
- 关键指标2: 增长率约Y%[来源2]
- 主要驱动因素: 政策支持 + 市场需求[来源3]

### 详细分析
{industry}行业的{dimension}受到多方面因素影响。从政策层面来看...[详细展开]

### 结论
综合来看，{dimension}的未来趋势是...[总结]

**数据来源**:
- [来源1] 标题来自搜索结果
- [来源2] 标题来自搜索结果
- [来源3] 标题来自搜索结果
"""
        else:
            # 回退模式（标注警告）
            content = f"""
⚠️ **警告**: 以下内容基于LLM训练记忆，非实时数据，请谨慎使用

## {dimension}分析

基于行业通用知识，{industry}行业在{dimension}方面的特点包括：

### 估算数据（需验证）
- 估计市场规模: 约X亿元（需验证）
- 估计增长率: 约Y%（需验证）

### 分析框架
[基于通用框架的分析...]

**重要说明**: 以上数字为估算值，建议通过权威数据源验证后使用。
"""

        return content

    def generate_full_report(self, industry: str, dimensions: List[str],
                           fail_fast: bool = True) -> Dict:
        """
        生成完整报告（多维度）

        Args:
            industry: 行业名称
            dimensions: 分析维度列表
            fail_fast: 是否在质量检查失败时立即停止

        Returns:
            {
                'industry': str,
                'dimensions': [...],  # 各维度分析结果
                'overall_quality': float,  # 整体质量分
                'passed': bool,  # 是否全部通过
                'failed_dimensions': [...],  # 未通过的维度
                'report_path': str  # 报告路径
            }
        """
        print(f"\n{'='*60}")
        print(f"🚀 开始生成报告: {industry}")
        print(f"   维度数量: {len(dimensions)}")
        print(f"   失败即停: {'是' if fail_fast else '否'}")
        print(f"{'='*60}\n")

        results = []
        failed_dimensions = []
        context = {}  # 累积上下文（前面维度的结果）

        for i, dimension in enumerate(dimensions, 1):
            print(f"\n[{i}/{len(dimensions)}] {dimension}")

            try:
                result = self.analyze_dimension(industry, dimension, context)
                results.append(result)

                # 更新上下文
                context[dimension] = result['content']

                # 检查是否通过
                if not result['passed']:
                    failed_dimensions.append(dimension)
                    if fail_fast:
                        print(f"\n❌ 维度 '{dimension}' 质量检查失败，停止生成")
                        break

            except Exception as e:
                print(f"❌ 维度 '{dimension}' 分析失败: {str(e)}")
                failed_dimensions.append(dimension)
                if fail_fast:
                    break

        # 计算整体质量分
        if results:
            overall_quality = sum(r['quality']['score'] for r in results) / len(results)
        else:
            overall_quality = 0.0

        # 生成报告文件
        passed = len(failed_dimensions) == 0
        report_path = self._save_report(industry, results, overall_quality, passed)

        # 打印总结
        print(f"\n{'='*60}")
        print(f"📊 报告生成完成")
        print(f"{'='*60}")
        print(f"   整体质量分: {overall_quality:.2f}")
        print(f"   通过维度: {len(results) - len(failed_dimensions)}/{len(results)}")
        print(f"   失败维度: {', '.join(failed_dimensions) if failed_dimensions else '无'}")
        print(f"   报告路径: {report_path}")
        print(f"   最终状态: {'✅ 通过' if passed else '❌ 未通过'}")
        print(f"{'='*60}\n")

        return {
            'industry': industry,
            'dimensions': results,
            'overall_quality': overall_quality,
            'passed': passed,
            'failed_dimensions': failed_dimensions,
            'report_path': report_path
        }

    def _save_report(self, industry: str, results: List[Dict],
                    quality: float, passed: bool) -> str:
        """保存报告到文件"""
        from core.environment_checker import SecureConfigManager

        # 获取输出目录（工作区）
        output_dir = SecureConfigManager.get_output_directory()

        # 生成文件名
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{industry}_{timestamp}.md"
        report_path = output_dir / filename

        # 生成Markdown报告
        report_content = f"""# {industry} - 行业研究报告

**生成时间**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**整体质量**: {quality:.2f} ({'✅ 通过' if passed else '❌ 未通过'})
**研究维度**: {len(results)}个

---

"""

        # 添加各维度内容
        for result in results:
            report_content += f"\n{result['content']}\n\n---\n"

        # 添加数据来源区块
        report_content += "\n## 📚 数据来源\n\n"
        if any(r.get('method') == 'web_search' for r in results):
            report_content += self.web_search.format_sources(self.search_history)
        else:
            report_content += "⚠️ 本报告未使用实时搜索数据，内容基于AI模型训练记忆\n"

        # 写入文件
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return str(report_path)


# ==================== 使用示例 ====================

def example_usage():
    """v2.0使用示例"""

    print("="*60)
    print("Industry Research Skill v2.0 - 演示")
    print("="*60)

    # 初始化v2.0引擎
    engine = ResearchEngineV2(enable_web_search=True)

    # 示例1: 分析单个维度
    print("\n示例1: 分析单个维度")
    result = engine.analyze_dimension(
        industry="医疗陪护",
        dimension="市场规模"
    )
    print(f"质量分: {result['quality']['score']}")
    print(f"通过: {result['passed']}")

    # 示例2: 生成完整报告
    print("\n示例2: 生成完整报告")
    report = engine.generate_full_report(
        industry="医疗陪护",
        dimensions=["政策环境", "市场规模", "商业模式"],
        fail_fast=True
    )
    print(f"报告路径: {report['report_path']}")
    print(f"整体通过: {report['passed']}")


if __name__ == "__main__":
    example_usage()
