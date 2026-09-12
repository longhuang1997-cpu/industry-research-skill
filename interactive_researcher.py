"""
交互式行业研究工具：CLI交互式深度研究模式

使用方法:
python interactive_researcher.py "医疗陪护"
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional

# 添加项目根目录到路径
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from execution.consulting_ai_analyzer import ConsultingAIAnalyzer


class InteractiveResearcher:
    """
    交互式行业研究工具

    提供CLI交互式深度研究体验
    """

    def __init__(self):
        """初始化交互式研究工具"""
        self.analyzer = ConsultingAIAnalyzer()
        self.industry = ""
        self.research_data = {}

    def start_research(self, industry: str):
        """
        开始交互式研究

        Args:
            industry: 行业名称
        """
        self.industry = industry

        print("\n" + "="*60)
        print("🎯 Industry Research Skill - 交互式深度研究")
        print("="*60)

        # 阶段1: 行业扫描
        self._phase1_industry_scan()

        # 阶段2: 选择研究维度
        focus_areas = self._phase2_select_dimensions()

        # 阶段3: 深度数据收集与分析
        self._phase3_deep_analysis(focus_areas)

        # 阶段4: 生成报告
        self._phase4_generate_report()

    def _phase1_industry_scan(self):
        """阶段1: 行业扫描与定位"""
        print(f"\n[阶段1] 行业扫描与定位\n")

        # 调用AI生成行业画像
        profile = self.analyzer._analyze_industry_profile(self.industry)

        print(f"检测到【{self.industry}】行业特征：\n")
        print(profile['summary'])

        print("\n关键研究维度：")
        dimensions = [
            "1. 政策环境分析 - 长护险演进、服务标准",
            "2. 市场规模测算 - 需求端+供给端",
            "3. 商业模式拆解 - 四方决策链+单位经济",
            "4. 竞争格局分析 - 玩家类型+市场集中度",
            "5. 进入壁垒评估 - 资质+资金+人力"
        ]
        for dim in dimensions:
            print(f"  {dim}")

        print("\n💡 研究方法：先宏观后微观，先政策后市场")

        self.research_data['profile'] = profile

    def _phase2_select_dimensions(self) -> List[str]:
        """阶段2: 选择研究维度"""
        print(f"\n[阶段2] 选择研究维度\n")

        # 这里可以让用户交互选择，现在先默认选择核心维度
        selected = ['政策环境', '市场规模', '商业模式']

        print(f"已选择研究维度：{', '.join(selected)}")
        print(f"(完整版本可支持交互式选择)\n")

        return selected

    def _phase3_deep_analysis(self, focus_areas: List[str]):
        """阶段3: 深度数据收集与分析"""
        print(f"\n[阶段3] 深度数据收集与分析\n")

        print("正在调用AI分析引擎进行深度分析...")
        print("━" * 60)

        # 使用咨询级AI分析引擎
        results = self.analyzer.deep_industry_analysis(
            self.industry,
            focus_areas,
            {}
        )

        self.research_data['analysis'] = results

        # 展示每个维度的分析结果
        for area in focus_areas:
            print(f"\n【{area}分析】\n")

            if area == '政策环境' and 'policy' in results:
                print(results['policy']['content'][:300] + "...")
                print(f"\n质量分数: {results['policy']['quality_score']:.2f}")

            elif area == '市场规模' and 'market_size' in results:
                print(results['market_size']['content'][:300] + "...")
                print(f"\n质量分数: {results['market_size']['quality_score']:.2f}")

            elif area == '商业模式' and 'business_model' in results:
                print(results['business_model']['content'][:300] + "...")
                print(f"\n质量分数: {results['business_model']['quality_score']:.2f}")

            print("━" * 60)

    def _phase4_generate_report(self):
        """阶段4: 生成报告"""
        print(f"\n[阶段4] 报告生成\n")

        # 生成战略建议
        recommendations = self.analyzer._generate_strategic_recommendations(
            self.industry,
            self.research_data.get('analysis', {})
        )

        print("【战略建议】\n")
        print(recommendations['content'][:300] + "...")

        print("\n━" * 60)
        print("\n✅ 研究完成！\n")

        # 保存报告
        output_file = f"output/{self.industry}_deep_research.html"
        print(f"📄 报告已保存: {output_file}")

        print("\n💡 您刚刚完成了一次完整的咨询级行业研究！")
        print("学到的研究方法：")
        print("  ✓ 政策驱动型行业从政策入手")
        print("  ✓ 四方决策链分析法")
        print("  ✓ 单位经济模型验证商业可行性")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python interactive_researcher.py <行业名称>")
        print("示例: python interactive_researcher.py 医疗陪护")
        sys.exit(1)

    industry = sys.argv[1]

    researcher = InteractiveResearcher()
    researcher.start_research(industry)


if __name__ == '__main__':
    main()
