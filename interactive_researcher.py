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

        # 生成HTML报告
        self._save_html_report(recommendations)

        print("\n💡 您刚刚完成了一次完整的咨询级行业研究！")
        print("学到的研究方法：")
        print("  ✓ 政策驱动型行业从政策入手")
        print("  ✓ 四方决策链分析法")
        print("  ✓ 单位经济模型验证商业可行性")

    def _save_html_report(self, recommendations):
        """保存HTML报告"""
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/{self.industry}_deep_research_{timestamp}.html"

        # 获取分析结果
        analysis = self.research_data.get('analysis', {})
        profile = self.research_data.get('profile', {})

        # 生成HTML内容
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.industry} - 深度行业研究报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-left: 4px solid #3498db; padding-left: 10px; }}
        .section {{ margin: 20px 0; padding: 15px; background: #ecf0f1; border-radius: 5px; }}
        .quality {{ color: #27ae60; font-weight: bold; }}
        .profile {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0; }}
        .footer {{ margin-top: 40px; text-align: center; color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{self.industry} 行业深度研究报告</h1>
        <p style="color: #7f8c8d;">生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <div class="profile">
            <h2>行业画像</h2>
            <p>{profile.get('summary', '暂无数据')}</p>
        </div>
"""

        # 添加各个分析维度
        if 'policy' in analysis:
            html_content += f"""
        <div class="section">
            <h2>政策环境分析</h2>
            <p class="quality">质量分数: {analysis['policy'].get('quality_score', 0):.2f}</p>
            <p>{analysis['policy'].get('content', '暂无数据')}</p>
        </div>
"""

        if 'market_size' in analysis:
            html_content += f"""
        <div class="section">
            <h2>市场规模测算</h2>
            <p class="quality">质量分数: {analysis['market_size'].get('quality_score', 0):.2f}</p>
            <p>{analysis['market_size'].get('content', '暂无数据')}</p>
        </div>
"""

        if 'business_model' in analysis:
            html_content += f"""
        <div class="section">
            <h2>商业模式分析</h2>
            <p class="quality">质量分数: {analysis['business_model'].get('quality_score', 0):.2f}</p>
            <p>{analysis['business_model'].get('content', '暂无数据')}</p>
        </div>
"""

        # 添加战略建议
        html_content += f"""
        <div class="section" style="background: #d4edda; border-left: 4px solid #28a745;">
            <h2>战略建议</h2>
            <p>{recommendations.get('content', '暂无数据')}</p>
        </div>

        <div class="footer">
            <p>本报告由 Industry Research Skill v0.3.0 生成</p>
            <p>AI驱动的咨询级行业研究工具</p>
        </div>
    </div>
</body>
</html>
"""

        # 确保output目录存在
        Path("output").mkdir(exist_ok=True)

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"📄 报告已保存: {output_file}")


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
