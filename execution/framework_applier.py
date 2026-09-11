"""
框架应用器：将选定的分析框架应用到收集的数据上

功能:
1. 根据框架选择器返回的框架列表
2. 将数据映射到各个框架的结构中
3. 使用AI分析引擎生成真实洞察
4. 生成结构化的分析结果
"""

import sys
from pathlib import Path
from typing import Dict, List

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from execution.ai_analyzer import AIAnalyzer


class FrameworkApplier:
    """
    框架应用器

    将分析框架应用到数据上，使用AI生成真实洞察
    """

    def __init__(self):
        """初始化框架应用器"""
        self.ai_analyzer = AIAnalyzer()

    def apply(self, frameworks: List[Dict], data: Dict) -> Dict:
        """
        应用框架到数据

        Args:
            frameworks: 框架列表（从框架选择器获取）
            data: 收集的数据

        Returns:
            analysis: 结构化的分析结果
        """
        print(f"\n[FrameworkApplier] Applying {len(frameworks)} frameworks...")

        analysis = {
            'frameworks': {},
            'summary': '',
            'insights': []
        }

        for fw in frameworks:
            fw_name = fw['name']
            print(f"   应用: {fw_name}...")

            # 根据框架类型调用不同的处理方法
            if fw_name == 'PEST分析':
                result = self._apply_pest(data, fw)
            elif fw_name == '行业链分析':
                result = self._apply_industry_chain(data, fw)
            elif fw_name == '四方决策链':
                result = self._apply_four_party(data, fw)
            elif fw_name == '单位经济模型':
                result = self._apply_unit_economics(data, fw)
            elif fw_name == '波特五力':
                result = self._apply_porter_five(data, fw)
            else:
                result = self._apply_generic(data, fw)

            analysis['frameworks'][fw_name] = result

        print(f"   [OK] Frameworks applied")

        return analysis

    def _apply_pest(self, data: Dict, framework: Dict) -> Dict:
        """应用PEST分析框架（使用AI生成真实洞察）"""
        industry = data.get('industry', '未知行业')

        # 使用AI分析引擎生成真实的PEST分析结论
        framework_questions = [
            '政策环境如何影响行业发展？',
            '经济因素对市场规模和增速有何影响？',
            '社会需求趋势是什么？',
            '技术创新的方向和影响？'
        ]

        conclusion = self.ai_analyzer.analyze_with_framework(
            'PEST分析',
            industry,
            data,
            framework_questions
        )

        return {
            'framework': 'PEST分析',
            'weight': framework['weight'],
            'conclusion': conclusion
        }

    def _extract_dimension(self, raw_data: List[Dict], keywords: List[str]) -> str:
        """从原始数据中提取特定维度的信息"""
        relevant_data = []

        for item in raw_data:
            data_text = str(item.get('data', ''))
            keyword_match = any(kw in data_text for kw in keywords)

            if keyword_match:
                relevant_data.append(data_text[:200])  # 限制长度

        if relevant_data:
            return ' | '.join(relevant_data[:3])  # 最多3条

        return None

    def _apply_industry_chain(self, data: Dict, framework: Dict) -> Dict:
        """应用行业链分析框架（使用AI生成真实洞察）"""
        industry = data.get('industry', '未知行业')

        framework_questions = [
            '上游供应商集中度如何？议价能力？',
            '中游竞争格局和关键瓶颈？',
            '下游需求特征和价格敏感度？'
        ]

        conclusion = self.ai_analyzer.analyze_with_framework(
            '行业链分析',
            industry,
            data,
            framework_questions
        )

        return {
            'framework': '行业链分析',
            'weight': framework['weight'],
            'conclusion': conclusion
        }

    def _apply_four_party(self, data: Dict, framework: Dict) -> Dict:
        """应用四方决策链框架（使用AI生成真实洞察）"""
        industry = data.get('industry', '未知行业')

        framework_questions = [
            '需求方、支付方、决策方分别是谁？',
            '三方利益诉求有何差异？',
            '供给方如何平衡多方需求？'
        ]

        conclusion = self.ai_analyzer.analyze_with_framework(
            '四方决策链',
            industry,
            data,
            framework_questions
        )

        return {
            'framework': '四方决策链',
            'weight': framework['weight'],
            'conclusion': conclusion
        }

    def _apply_unit_economics(self, data: Dict, framework: Dict) -> Dict:
        """应用单位经济模型框架（使用AI生成真实洞察）"""
        industry = data.get('industry', '未知行业')

        framework_questions = [
            '获客成本(CAC)水平如何？',
            '人力成本占比多少？',
            '毛利率和盈利能力？',
            '客户终身价值(LTV)如何？'
        ]

        conclusion = self.ai_analyzer.analyze_with_framework(
            '单位经济模型',
            industry,
            data,
            framework_questions
        )

        return {
            'framework': '单位经济模型',
            'weight': framework['weight'],
            'conclusion': conclusion
        }

    def _apply_porter_five(self, data: Dict, framework: Dict) -> Dict:
        """应用波特五力框架（使用AI生成真实洞察）"""
        industry = data.get('industry', '未知行业')

        framework_questions = [
            '现有竞争者竞争强度？',
            '新进入者威胁大小？',
            '替代品威胁如何？',
            '供应商和客户议价能力？'
        ]

        conclusion = self.ai_analyzer.analyze_with_framework(
            '波特五力',
            industry,
            data,
            framework_questions
        )

        return {
            'framework': '波特五力',
            'weight': framework['weight'],
            'conclusion': conclusion
        }

    def _apply_generic(self, data: Dict, framework: Dict) -> Dict:
        """通用框架应用"""
        return {
            'framework': framework['name'],
            'weight': framework['weight'],
            'result': f"{framework['name']}分析结果（待实现）",
            'conclusion': f"{framework['name']}结论（待实现）"
        }


def main():
    """测试框架应用器"""
    from knowledge.frameworks.framework_selector import FrameworkSelector

    print("="*60)
    print("测试: 框架应用器")
    print("="*60)

    # 初始化
    selector = FrameworkSelector()
    applier = FrameworkApplier()

    # 选择框架
    frameworks = selector.select_frameworks('医疗陪护')

    # 模拟数据
    mock_data = {
        'raw_data': [],
        'sources': [],
        'tier1_coverage': 0.3
    }

    # 应用框架
    analysis = applier.apply(frameworks, mock_data)

    print("\n分析结果:")
    for fw_name, result in analysis['frameworks'].items():
        print(f"\n  {fw_name} (权重{result['weight']})")
        print(f"    结论: {result.get('conclusion', 'N/A')}")


if __name__ == '__main__':
    main()
